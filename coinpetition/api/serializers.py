from rest_framework import serializers
from .models import GameSession, GameCoin, CoinValueHistory, FinanceQuestion


class CoinValueHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CoinValueHistory
        fields = ['timestamp', 'value']


class GameCoinSerializer(serializers.ModelSerializer):
    value_history = CoinValueHistorySerializer(many=True, read_only=True)
    
    class Meta:
        model = GameCoin
        fields = ['coin_name', 'current_value', 'value_history']


class GameSessionSerializer(serializers.ModelSerializer):
    coins = GameCoinSerializer(many=True, read_only=True)
    
    class Meta:
        model = GameSession
        fields = ['session_id', 'created_at', 'updated_at', 'coins']


class FinanceQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinanceQuestion
        fields = ['question', 'options', 'correct_answer', 'explanation']
