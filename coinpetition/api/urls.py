from django.urls import path
from .views import GameSessionView, CoinSituationView, FinanceQuestionView, SituationAnswerView, UserView

urlpatterns = [
    path('game', GameSessionView.as_view(), name='game_session'),
    path('game/<str:session_id>/', GameSessionView.as_view(), name='game_session'),
    path('game/<str:session_id>/coin/<str:coin_name>/situation/', CoinSituationView.as_view(), name='coin_situation'),
    path('game/<str:session_id>/coin/<str:coin_name>/finance_question/', FinanceQuestionView.as_view(), name='finance_question'),
    path('situation/<int:situation_id>/answer/', SituationAnswerView.as_view(), name='situation_answer'),
    path('user/<str:name>/', UserView.as_view(), name='user'),
]
