from django.urls import path
from .views import GameSessionView, CoinSituationView

urlpatterns = [
    path('game/<str:session_id>/', GameSessionView.as_view(), name='game_session'),
    path('game/<str:session_id>/coin/<str:coin_name>/situation/', CoinSituationView.as_view(), name='coin_situation'),
]
