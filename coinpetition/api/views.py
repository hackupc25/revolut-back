from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from datetime import date
from json import loads
from django.utils import timezone

from .models import (
    GameSession, GameCoin, FinanceQuestion, FinanceQuestionAnswer,
    Situation, CoinValueHistory
)
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

        # Use the game situation generator
        situation_data = get_game_situation(
            coin_name=coin.coin_name,
            coin_value=coin.current_value,
        )
        print(situation_data)

        # Convert Gemini model objects to standard Python data types
        serializable_choices = []
        for choice in situation_data["choices"]:
            serializable_choices.append({
                "id": str(choice["id"]),
                "text": str(choice["text"]),
                "consequence": str(choice["consequence"]),
                "updated_value": float(choice["updated_value"]),
            })

        # Get the latest value history or create one if it doesn't exist
        # first() because ordering is already by -timestamp
        latest_value_history = coin.value_history.first()
        if not latest_value_history:
            # If no history exists, create one with the current timestamp
            latest_value_history = coin.value_history.create(
                timestamp=timezone.now(),
                value=coin.current_value
            )

        situation = Situation.objects.create(
            coin_value_history=latest_value_history,
            category=str(situation_data["category"]),
            description=str(situation_data["situation"]),
            choices=serializable_choices
        )

        # Format the response
        response_data = {
            "id": situation.id,
            "coin_name": coin.coin_name,
            "situation": situation.description,
            "category": situation.category,
            "choices": [
                {
                    "id": situation.choices[0]["id"],
                    "text": situation.choices[0]["text"],
                    "consequence": situation.choices[0]["consequence"],
                    "updated_value": situation.choices[0]["updated_value"]
                },
                {
                    "id": situation.choices[1]["id"],
                    "text": situation.choices[1]["text"],
                    "consequence": situation.choices[1]["consequence"],
                    "updated_value": situation.choices[1]["updated_value"]
                }
            ]
        }

        return Response(response_data)


class FinanceQuestionView(APIView):
    """
    API view to get a finance question
    """
    def get(self, request, session_id):
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

        return Response({"question": question.question, "options": question.options}, status=status.HTTP_200_OK)
    
    def post(self, request, session_id):
        game_session = get_object_or_404(GameSession, session_id=session_id)
        question = FinanceQuestion.objects.filter(date=date.today()).first()
        answer = request.data.get("answer")
        correct = question.correct_answer == answer

        FinanceQuestionAnswer.objects.create(
            question=question, 
            answer=answer, 
            correct=correct, 
            user=game_session
        )

        return Response({"correct_answer": question.correct_answer, "explanation": question.explanation}, status=status.HTTP_200_OK)


class SituationAnswerView(APIView):
    """
    API view to get a situation answer
    """
    def post(self, request, session_id, coin_name, situation_id):
        game_session = get_object_or_404(GameSession, session_id=session_id)
        coin = get_object_or_404(GameCoin, game_session=game_session, coin_name=coin_name)
        # Get the situation and ensure it belongs to this coin's value history
        situation = get_object_or_404(Situation, id=situation_id)
        if situation.coin_value_history.coin != coin:
            return Response({"error": "Situation does not belong to this coin"}, status=status.HTTP_400_BAD_REQUEST)

        request_choice = request.data.get("choice")
        
        for choice in situation.choices:
            if choice["id"] == request_choice:
                # Update the situation with the selected choice
                situation.selected_choice = request_choice
                situation.save()
                
                # Create a new historical record with the updated value
                new_value = float(choice["updated_value"])
                CoinValueHistory.objects.create(
                    coin=coin,
                    timestamp=timezone.now(),
                    value=coin.current_value
                )
                
                # Update the coin's current value
                coin.current_value = new_value
                coin.save()
                
                return Response(
                    {"consequence": choice["consequence"]},
                    status=status.HTTP_200_OK
                )

        return Response(
            {"error": "Invalid choice selected"},
            status=status.HTTP_400_BAD_REQUEST
        )