from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views import generic
# Create your views here.

from .models import Movie


SORTING_CHOICES = {
    "popular": "popular",
    "unpopular": "unpopular",
    "top rated": "-rating_avg",
    "low rated": "rating_avg",
    "recent": "-release_date",
    "old": "release_date",
}

class MovieListView(generic.ListView):
    # model = Movie

    paginate_by = 100

    def get_queryset(self) -> QuerySet[Any]:
        request = self.request
        sort = request.GET.get('sort') or \
            request.session.get('movie_sort_order', '-rating_avg') or \
                "popular"
        qs = Movie.objects.all()
        if sort is not None:
            request.session['movie_sort_order'] = sort
            if sort == "popular":
                return qs.popular()
            elif sort == "unpopular":
                return qs.popular(reverse=True)
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


class MovieInfiniteRatingView(MovieDetailView):
    def get_object(self):
        user = self.request.user
        # exclude_ids = []
        # if user.is_authenticated:
        #     exclude_ids = [x.object_id for x in user.rating_set.filter(active=True)]
        # return Movie.objects.all().exclude(id__in=exclude_ids).order_by('?').first()
        return Movie.objects.all().order_by('?').first()

    def get_template_names(self):
        request = self.request 
        if request.htmx:
            return ['movies/snippet/infinite.html',]
        return ['movies/infinite-view.html', ]


movie_infinite_rating_view = MovieInfiniteRatingView.as_view()


class MoviePopularView(MovieDetailView):
    def get_context_data(self, **kwargs: Any):
        context =  super().get_context_data(**kwargs)
        context['endless_path'] = '/movies/popular/'
        return context

    def get_object(self):
        user = self.request.user
        exclude_ids = []
        if user.is_authenticated:
            exclude_ids = [x.object_id for x in user.rating_set.filter(active=True)]

        movie_id_options = Movie.objects.all().popular().exclude(id__in=exclude_ids).values_list("id", flat=True)[:250]
        return Movie.objects.filter(id__in=movie_id_options).order_by('?').first()

    def get_template_names(self):
        request = self.request 
        if request.htmx:
            return ['movies/snippet/infinite.html',]
        return ['movies/infinite-view.html', ]


movie_popular_view = MoviePopularView.as_view()