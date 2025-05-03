from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import GameSession, GameCoin
from .serializers import GameSessionSerializer
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
