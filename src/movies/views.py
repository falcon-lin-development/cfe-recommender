from typing import Any
from django.shortcuts import render
from django.views import generic
# Create your views here.

from .models import Movie

class MovieListView(generic.ListView):
    # model = Movie
    template_name = 'movies/movie_list.html'
    queryset = Movie.objects.all().order_by('-rating_avg')
    paginate_by = 100

    # def get_context_data(self, **kwargs: Any):
    #     context = super().get_context_data(**kwargs)
    #     print(context)
    #     return context


movie_list_view = MovieListView.as_view()

class MovieDetailView(generic.DetailView):
    model = Movie
    template_name = 'movies/movie_detail.html'

movie_detail_view = MovieDetailView.as_view()