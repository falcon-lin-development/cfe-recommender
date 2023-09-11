from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views import generic
# Create your views here.

from .models import Movie


SORTING_CHOICES = {
    "popular": "-rating_avg",
    "unpopular": "rating_avg",
    "recent": "-release_date",
    "old": "release_date",
}

class MovieListView(generic.ListView):
    # model = Movie

    paginate_by = 100

    def get_queryset(self) -> QuerySet[Any]:
        request = self.request
        default_sort = request.session.get('movie_sort_order', '-rating_avg')
        qs = Movie.objects.all().order_by(default_sort)
        sort = request.GET.get('sort')
        if sort is not None:
            request.session['movie_sort_order'] = sort
            qs = qs.order_by(sort)
        return qs

    def get_template_names(self):
        request = self.request 
        if request.htmx:
            return ['movies/snippet/list.html',]
        return ['movies/movie_list.html', ]

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        request = self.request
        user = request.user
        context["sorting_choices"] = SORTING_CHOICES
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