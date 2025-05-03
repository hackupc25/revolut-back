from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import GameSession, GameCoin
from .serializers import GameSessionSerializer


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
        coin = get_object_or_404(GameCoin, game_session=game_session, coin_name=coin_name)
        
        # Dummy implementation - will be replaced later
        situation = {
            "coin_name": coin.coin_name,
            "event_type": "price_movement",
            "description": "The coin value is increasing rapidly due to market demand!",
            "impact": "positive"
        }
        
        return Response(situation)
