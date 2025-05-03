from rest_framework import serializers
from .models import GameSession, GameEvent


class GameEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameEvent
        fields = '__all__'


class GameSessionSerializer(serializers.ModelSerializer):
    events = GameEventSerializer(many=True, read_only=True)
    
    class Meta:
        model = GameSession
        fields = '__all__'


class SituationRequestSerializer(serializers.Serializer):
    session_id = serializers.CharField(required=True)


class ChoiceRequestSerializer(serializers.Serializer):
    session_id = serializers.CharField(required=True)
    choice = serializers.CharField(required=True)
    situation_data = serializers.JSONField(required=True)


class NewGameSerializer(serializers.Serializer):
    coin_name = serializers.CharField(required=True)
    initial_value = serializers.FloatField(required=True) 