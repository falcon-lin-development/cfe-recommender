from django.shortcuts import render
from django.views import generic
# Create your views here.

from .models import Movie

class MovieListView(generic.ListView):
    model = Movie
    template_name = 'movies/movie_list.html'
    queryset = Movie.objects.all().order_by('-rating_avg')
    paginate_by = 100


movie_list_view = MovieListView.as_view()

class MovieDetailView(generic.DetailView):
    model = Movie
    template_name = 'movies/movie_detail.html'

movie_detail_view = MovieDetailView.as_view()