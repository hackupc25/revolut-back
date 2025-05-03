from django.db import models


class GameSession(models.Model):
    """Model to track a game session."""

    session_id = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class GameCoin(models.Model):
    """Model to track a coin in a game session."""

    game_session = models.ForeignKey(
        GameSession, related_name="coins", on_delete=models.CASCADE
    )
    coin_name = models.CharField(max_length=100)


class GamePlayer(models.Model):
    """Model to track a player in a game session."""

    game_session = models.ForeignKey(
        GameSession,
        related_name="players",
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100)
    coin = models.ForeignKey(
        GameCoin,
        related_name="players",
        on_delete=models.CASCADE
    )


class CoinValueHistory(models.Model):
    """Model to track historical values of a coin over time."""

    coin = models.ForeignKey(
        GameCoin, related_name="value_history", on_delete=models.CASCADE
    )
    timestamp = models.DateTimeField()
    value = models.FloatField()

    class Meta:
        indexes = [
            models.Index(fields=["coin", "timestamp"]),
        ]
        ordering = ["-timestamp"]
        get_latest_by = "timestamp"


class FinanceQuestion(models.Model):
    """Model to track a finance question."""

    question = models.TextField()
    options = models.JSONField()
    correct_answer = models.CharField(max_length=1)
    explanation = models.TextField()
    date = models.DateField(auto_now_add=True)


class FinanceQuestionAnswer(models.Model):
    """Model to track the answers to the finance questions for each user"""

    question = models.ForeignKey(
        FinanceQuestion, related_name="question_answer", on_delete=models.CASCADE
    )
    answer = models.CharField(max_length=1)
    correct = models.BooleanField(default=False)
    user = models.ForeignKey(
        GameCoin, related_name="question_answer", on_delete=models.CASCADE
    )


class Situation(models.Model):
    """Model to track situations linked to coin value history."""

    coin = models.ForeignKey(
        GameCoin, related_name="situations", on_delete=models.CASCADE
    )
    category = models.CharField(max_length=50)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    initial_value = models.FloatField()

    choices = models.JSONField()

    selected_choice = models.CharField(
        max_length=1, choices=[("A", "A"), ("B", "B")], null=True, blank=True
    )

    class Meta:
        indexes = [
            models.Index(fields=["coin", "created_at"]),
        ]
        ordering = ["-created_at"]
