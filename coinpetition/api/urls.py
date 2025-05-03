from django.urls import path
from .views import GameSessionView, CoinSituationView, FinanceQuestionView

urlpatterns = [
    path('game/<str:session_id>/', GameSessionView.as_view(), name='game_session'),
    path('game/<str:session_id>/coin/<str:coin_name>/get_situation/', CoinSituationView.as_view(), name='coin_situation'),
    path('game/<str:session_id>/finance_question/', FinanceQuestionView.as_view(), name='finance_question'),
]
