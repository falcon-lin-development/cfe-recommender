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

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        request = self.request
        user = request.user
        if user.is_authenticated:
            obj_ids = [x.id for x in context["object_list"]]
            context['my_ratings'] = user.rating_set.filter(active=True).as_object_dict(object_ids=obj_ids)

        return context


movie_list_view = MovieListView.as_view()

class MovieDetailView(generic.DetailView):
    model = Movie
    template_name = 'movies/movie_detail.html'

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        request = self.request
        user = request.user
        if user.is_authenticated:
            obj_ids = [context["object"].id, ]
            context['my_ratings'] = user.rating_set.filter(active=True).as_object_dict(object_ids=obj_ids)

        return context


movie_detail_view = MovieDetailView.as_view()