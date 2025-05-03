from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from datetime import date
from json import loads

from .models import GameSession, GameCoin, FinanceQuestion, FinanceQuestionAnswer
from .serializers import GameSessionSerializer
from coinpetition.finance_question_generator import generate_question
from .utils.game_situation_generator import get_game_situation


class GameSessionView(APIView):
    """
    API view to return all coins from a session with their historical values
    """
    def get(self, request, session_id):
        game_session = get_object_or_404(GameSession, session_id=session_id)
        serializer = GameSessionSerializer(game_session)
        return Response(serializer.data)


class CoinSituationView(APIView):
    """
    API view to get a situation event for a specific coin
    """
    def get(self, request, session_id, coin_name):
        game_session = get_object_or_404(GameSession, session_id=session_id)
        coin = get_object_or_404(
            GameCoin, game_session=game_session, coin_name=coin_name
        )
        
        # Get the coin history from the database
        coin_history = []
        for event in coin.history.all().order_by('-created_at'):
            coin_history.append({
                "situation": event.situation,
                "category": event.category,
                "choice": event.choice,
                "consequence": event.consequence,
                "value_after": event.value_after
            })
        
        # Use the new game situation generator
        choices = get_game_situation(
            coin_name=coin.coin_name,
            coin_value=coin.current_value,
            history=coin_history
        )
        
        # Format the response
        response_data = {
            "coin_name": coin.coin_name,
            "situation": choices[0]["situation"],
            "category": choices[0]["category"],
            "choices": [
                {
                    "id": "A",
                    "text": choices[0]["choice_text"],
                    "consequence": choices[0]["consequence"],
                    "updated_value": choices[0]["updated_value"]
                },
                {
                    "id": "B",
                    "text": choices[1]["choice_text"],
                    "consequence": choices[1]["consequence"],
                    "updated_value": choices[1]["updated_value"]
                }
            ]
        }
        
        return Response(response_data)
    
    def post(self, request, session_id, coin_name):
        game_session = get_object_or_404(GameSession, session_id=session_id)
        coin = get_object_or_404(
            GameCoin, game_session=game_session, coin_name=coin_name
        )
        
        # Process the user's choice
        choice_id = request.data.get("choice_id", "").upper()
        situation = request.data.get("situation", "")
        category = request.data.get("category", "")
        choice_text = request.data.get("choice_text", "")
        consequence = request.data.get("consequence", "")
        updated_value = float(request.data.get("updated_value", 0))
        
        # Update the coin value
        value_change = updated_value - coin.current_value
        coin.current_value = updated_value
        coin.save()
        
        # Record the event in history
        coin.history.create(
            situation=situation,
            category=category,
            choice=f"{choice_id}: {choice_text}",
            consequence=consequence,
            value_after=updated_value
        )
        
        return Response({
            "coin_name": coin.coin_name,
            "new_value": coin.current_value,
            "value_change": value_change
        })


class FinanceQuestionView(APIView):
    """
    API view to get a finance question
    """
    def get(self, request, session_id, coin_name):
        game_session = get_object_or_404(GameSession, session_id=session_id)
        question = FinanceQuestion.objects.filter(date=date.today()).first()
        if not question:
            raw_llm_response = generate_question()
            if raw_llm_response.startswith("```json"):
                cleaned_response = raw_llm_response.strip().replace("```json", "").replace("```", "").strip()
            else:
                 cleaned_response = raw_llm_response # Assume it's already valid JSON if no fences

            try:
                question_data = loads(cleaned_response)
            except Exception as e:
                print(f"Error parsing cleaned LLM response: {e}\nResponse: {cleaned_response}")
                return Response({"error": "Failed to parse finance question from LLM"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            question = FinanceQuestion.objects.create(
                question=question_data["question"],
                options=question_data["options"],
                correct_answer=question_data["correct_answer"],
                explanation=question_data["explanation"]
            )

        return Response({"question": question.question, "answers": question.options}, status=status.HTTP_200_OK)
    
    def post(self, request, session_id, coin_name):
        game_session = get_object_or_404(GameSession, session_id=session_id)
        coin = get_object_or_404(GameCoin, game_session=game_session, coin_name=coin_name)
        question = FinanceQuestion.objects.filter(date=date.today()).first()
        answer = request.data.get("answer")
        correct = question.correct_answer == answer

        FinanceQuestionAnswer.objects.create(
            question=question, 
            answer=answer, 
            correct=correct, 
            user=coin
        )

        return Response({"correct_answer": question.correct_answer, "explanation": question.explanation}, status=status.HTTP_200_OK)

        
