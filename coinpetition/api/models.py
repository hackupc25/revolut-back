from django.db import models


class GameSession(models.Model):
    """Model to track a game session."""
    session_id = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class GameCoin(models.Model):
    """Model to track a coin in a game session."""
    game_session = models.ForeignKey(
        GameSession, 
        related_name='coins', 
        on_delete=models.CASCADE
    )
    coin_name = models.CharField(max_length=100)
    current_value = models.FloatField(default=0.0)


class CoinValueHistory(models.Model):
    """Model to track historical values of a coin over time."""
    coin = models.ForeignKey(
        GameCoin,
        related_name='value_history',
        on_delete=models.CASCADE
    )
    timestamp = models.DateTimeField()
    value = models.FloatField()
    
    class Meta:
        indexes = [
            models.Index(fields=['coin', 'timestamp']),
        ]
        ordering = ['-timestamp']
