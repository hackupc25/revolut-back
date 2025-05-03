from django.db import models

# Create your models here.

class GameSession(models.Model):
    """Model to track a game session."""
    session_id = models.CharField(max_length=100, unique=True)
    coin_name = models.CharField(max_length=100)
    coin_value = models.FloatField()
    popularity = models.IntegerField(default=50)
    tech_innovation = models.IntegerField(default=50)
    regulation_risk = models.IntegerField(default=50)
    investor_confidence = models.IntegerField(default=50)
    global_adoption = models.IntegerField(default=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.coin_name} (Session: {self.session_id})"


class GameEvent(models.Model):
    """Model to store each game event."""
    game_session = models.ForeignKey(GameSession, on_delete=models.CASCADE, related_name='events')
    situation = models.TextField()
    category = models.CharField(max_length=50)
    choice = models.TextField()
    consequence = models.TextField()
    value_after = models.FloatField()
    popularity_after = models.IntegerField()
    tech_innovation_after = models.IntegerField()
    regulation_risk_after = models.IntegerField()
    investor_confidence_after = models.IntegerField()
    global_adoption_after = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Event {self.id} for {self.game_session}"
