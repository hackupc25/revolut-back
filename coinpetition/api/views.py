from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from datetime import date
from json import loads

from .models import GameSession, GameCoin, FinanceQuestion
from .serializers import GameSessionSerializer, FinanceQuestionSerializer
from coinpetition.finance_question_generator import generate_question
from .utils.game_situation_generator import GameState, generate_situation, parse_situation_response


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
        
        # Use game situation generator to create a relevant situation
        game_state = GameState(coin.coin_name, coin.current_value)
        situation_text = generate_situation(game_state)
        situation, category, choice_a, choice_b = parse_situation_response(
            situation_text
        )
        
        response_data = {
            "coin_name": coin.coin_name,
            "situation": situation,
            "category": category,
            "choices": [
                {
                    "id": "A",
                    "text": choice_a.get("text", ""),
                    "consequence": choice_a.get("consequence", "")
                },
                {
                    "id": "B",
                    "text": choice_b.get("text", ""),
                    "consequence": choice_b.get("consequence", "")
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
                # Handle potential JSON parsing errors after cleaning
                print(f"Error parsing cleaned LLM response: {e}\nResponse: {cleaned_response}")
                return Response({"error": "Failed to parse finance question from LLM"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            question = FinanceQuestion.objects.create(
                question=question_data["question"],
                options=question_data["options"],
                correct_answer=question_data["correct_answer"],
                explanation=question_data["explanation"]
            )

        serializer = FinanceQuestionSerializer(question)
        return Response(serializer.data)
