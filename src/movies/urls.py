
from django.contrib import admin
from django.urls import path
from .views import movie_list_view, movie_detail_view, movie_infinite_rating_view, movie_popular_view

urlpatterns = [
    path('', movie_list_view, name='movie-list'),
    path('infinite/', movie_infinite_rating_view, name='movie-infinite-rating'),
    path('popular/', movie_popular_view, name='movie-popular'),

    path('<int:pk>/', movie_detail_view, name='movie-detail'),
]
