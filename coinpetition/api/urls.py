from django.urls import path
from .views import NewGameView, GenerateSituationView, MakeChoiceView, GameStateView

urlpatterns = [
    path('game/new/', NewGameView.as_view(), name='new_game'),
    path('game/situation/', GenerateSituationView.as_view(), name='generate_situation'),
    path('game/choice/', MakeChoiceView.as_view(), name='make_choice'),
    path('game/state/<str:session_id>/', GameStateView.as_view(), name='game_state'),
] 