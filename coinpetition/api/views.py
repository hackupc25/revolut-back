from django.shortcuts import render
import uuid
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from coinpetition.game_situation_generator import GameState, generate_situation, parse_situation_response, apply_choice
from .models import GameSession, GameEvent
from .serializers import (
    GameSessionSerializer, 
    GameEventSerializer, 
    SituationRequestSerializer,
    ChoiceRequestSerializer,
    NewGameSerializer
)


class NewGameView(APIView):
    """API endpoint to start a new game."""
    
    def post(self, request):
        serializer = NewGameSerializer(data=request.data)
        if serializer.is_valid():
            coin_name = serializer.validated_data['coin_name']
            initial_value = serializer.validated_data['initial_value']
            
            # Generate unique session ID
            session_id = str(uuid.uuid4())
            
            # Create new game session
            game_session = GameSession.objects.create(
                session_id=session_id,
                coin_name=coin_name,
                coin_value=initial_value
            )
            
            return Response({
                'session_id': session_id,
                'game': GameSessionSerializer(game_session).data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GenerateSituationView(APIView):
    """API endpoint to generate a new game situation."""
    
    def post(self, request):
        serializer = SituationRequestSerializer(data=request.data)
        if serializer.is_valid():
            session_id = serializer.validated_data['session_id']
            
            try:
                # Get game session
                game_session = GameSession.objects.get(session_id=session_id)
                
                # Create game state object for situation generator
                game_state = GameState(game_session.coin_name, game_session.coin_value)
                
                # Add previous events to game state
                events = GameEvent.objects.filter(game_session=game_session).order_by('created_at')
                for event in events:
                    metrics_after = {
                        'popularity': event.popularity_after,
                        'tech_innovation': event.tech_innovation_after,
                        'regulation_risk': event.regulation_risk_after,
                        'investor_confidence': event.investor_confidence_after,
                        'global_adoption': event.global_adoption_after,
                    }
                    game_state.metrics = metrics_after
                    game_state.event_categories.append(event.category)
                    game_state.coin_value = event.value_after
                
                # Generate new situation
                response_text = generate_situation(game_state)
                situation, category, choice_a, choice_b = parse_situation_response(response_text)
                
                return Response({
                    'situation': situation,
                    'category': category,
                    'choices': {
                        'A': {
                            'text': choice_a.get('text', ''),
                            'consequence': choice_a.get('consequence', ''),
                            'new_value': choice_a.get('new_value', 0),
                            'metrics': choice_a.get('metrics', {})
                        },
                        'B': {
                            'text': choice_b.get('text', ''),
                            'consequence': choice_b.get('consequence', ''),
                            'new_value': choice_b.get('new_value', 0),
                            'metrics': choice_b.get('metrics', {})
                        }
                    }
                }, status=status.HTTP_200_OK)
                
            except GameSession.DoesNotExist:
                return Response({'error': 'Game session not found'}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MakeChoiceView(APIView):
    """API endpoint to make a choice and apply consequences."""
    
    def post(self, request):
        serializer = ChoiceRequestSerializer(data=request.data)
        if serializer.is_valid():
            session_id = serializer.validated_data['session_id']
            choice_letter = serializer.validated_data['choice']
            situation_data = serializer.validated_data['situation_data']
            
            try:
                # Get game session
                game_session = GameSession.objects.get(session_id=session_id)
                
                # Create game state object
                game_state = GameState(game_session.coin_name, game_session.coin_value)
                
                # Add previous events to game state
                events = GameEvent.objects.filter(game_session=game_session).order_by('created_at')
                for event in events:
                    metrics_after = {
                        'popularity': event.popularity_after,
                        'tech_innovation': event.tech_innovation_after,
                        'regulation_risk': event.regulation_risk_after,
                        'investor_confidence': event.investor_confidence_after,
                        'global_adoption': event.global_adoption_after,
                    }
                    game_state.metrics = metrics_after
                    game_state.event_categories.append(event.category)
                    game_state.coin_value = event.value_after
                
                # Get situation data
                situation = situation_data.get('situation', '')
                category = situation_data.get('category', '')
                choices = situation_data.get('choices', {})
                
                # Apply the choice
                if choice_letter == 'A' and 'A' in choices:
                    choice_data = choices['A']
                    apply_choice(game_state, situation, category, choice_data, 'A')
                elif choice_letter == 'B' and 'B' in choices:
                    choice_data = choices['B']
                    apply_choice(game_state, situation, category, choice_data, 'B')
                else:
                    return Response({'error': 'Invalid choice'}, status=status.HTTP_400_BAD_REQUEST)
                
                # Update game session
                game_session.coin_value = game_state.coin_value
                game_session.popularity = game_state.metrics['popularity']
                game_session.tech_innovation = game_state.metrics['tech_innovation']
                game_session.regulation_risk = game_state.metrics['regulation_risk']
                game_session.investor_confidence = game_state.metrics['investor_confidence']
                game_session.global_adoption = game_state.metrics['global_adoption']
                game_session.save()
                
                # Create new event
                choice_text = choice_data.get('text', '')
                consequence = choice_data.get('consequence', '')
                
                event = GameEvent.objects.create(
                    game_session=game_session,
                    situation=situation,
                    category=category,
                    choice=f"{choice_letter}: {choice_text}",
                    consequence=consequence,
                    value_after=game_state.coin_value,
                    popularity_after=game_state.metrics['popularity'],
                    tech_innovation_after=game_state.metrics['tech_innovation'],
                    regulation_risk_after=game_state.metrics['regulation_risk'],
                    investor_confidence_after=game_state.metrics['investor_confidence'],
                    global_adoption_after=game_state.metrics['global_adoption']
                )
                
                return Response({
                    'game': GameSessionSerializer(game_session).data,
                    'event': GameEventSerializer(event).data
                }, status=status.HTTP_200_OK)
                
            except GameSession.DoesNotExist:
                return Response({'error': 'Game session not found'}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GameStateView(APIView):
    """API endpoint to get current game state."""
    
    def get(self, request, session_id):
        try:
            game_session = GameSession.objects.get(session_id=session_id)
            return Response(GameSessionSerializer(game_session).data, status=status.HTTP_200_OK)
        except GameSession.DoesNotExist:
            return Response({'error': 'Game session not found'}, status=status.HTTP_404_NOT_FOUND)
