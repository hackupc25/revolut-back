from django.contrib import admin
from .models import GameSession, GameCoin, CoinValueHistory

# Register your models here.
admin.site.register(GameSession)
admin.site.register(GameCoin)
admin.site.register(CoinValueHistory)
