from django.urls import path
from . import views

app_name = 'game'

urlpatterns = [
    path('', views.home, name='home'),
    path('number-sequence/', views.number_sequence, name='number_sequence'),
    path('check/<int:game_id>/', views.check_sequence, name='check_sequence'),
    path('reset/<int:game_id>/', views.reset_game, name='reset_game'),
    path('color-pairs/', views.color_pairs, name='color_pairs'),
    path('check-pairs/<int:game_id>/', views.check_pairs, name='check_pairs'),
    path('reset-pairs/<int:game_id>/', views.reset_pairs, name='reset_pairs'),
    path('directional-memory/', views.directional_memory, name='directional_memory'),
    path('check-direction/<int:game_id>/', views.check_direction, name='check_direction'),
    path('reset-direction/<int:game_id>/', views.reset_direction, name='reset_direction'),
] 