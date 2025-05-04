from rest_framework import serializers
from .models import GameSession, GameCoin, CoinValueHistory, FinanceQuestion, GamePlayer


class CoinValueHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CoinValueHistory
        fields = ['timestamp', 'value']


class GameCoinSerializer(serializers.ModelSerializer):
    value_history = CoinValueHistorySerializer(many=True, read_only=True)
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = GameCoin
        fields = ['coin_name', 'description', 'image', 'value_history']
    
    def get_image(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request is not None:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


class GameSessionSerializer(serializers.ModelSerializer):
    coins = GameCoinSerializer(many=True, read_only=True)
    
    class Meta:
        model = GameSession
        fields = ['session_id', 'created_at', 'updated_at', 'coins']


class FinanceQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinanceQuestion
        fields = ['question', 'options', 'correct_answer', 'explanation']


class GamePlayerSerializer(serializers.ModelSerializer):
    session_id = serializers.ReadOnlyField(source='game_session.session_id')
    coin_name = serializers.ReadOnlyField(source='coin.coin_name')

    class Meta:
        model = GamePlayer
        fields = ['name', 'coin_name', 'session_id']

