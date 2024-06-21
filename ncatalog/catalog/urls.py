from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('home', home, name='home'),
    path('like/<int:game_id>/', like_game, name='like_game'),
    path('comment/<int:game_id>/', comment_game, name='comment_game'),
    path('add/', add_game, name='add_game'),
    path('edit/<int:game_id>/', edit_game, name='edit_game'),
    path('delete/<int:game_id>/', delete_game, name='delete_game'),
]