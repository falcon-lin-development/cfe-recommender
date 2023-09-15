from celery import shared_task
from django.apps import apps
from django.db.models import Window, F
from django.db.models.functions import DenseRank
# from .models import Movie

@shared_task
def update_movie_position_embedding_idx():
    Movie = apps.get_model('movies', 'Movie')
    qs = Movie.objects.all().annotate(
        new_idx=Window(
            expression=DenseRank(),
            order_by=[F("id").asc()]
        )
    ).annotate(
        final_idx=F("new_idx")-1
    )
    updated = 0
    for obj in qs:
        if obj.final_idx != obj.idx:
            updated += 1
            obj.idx = obj.final_idx
            obj.save(update_fields=['idx'])
    print("Updated", updated, "movies")


# @shared_task(name='task_calculate_movie_ratings')
# def task_calculate_movie_ratings(all=False, count=None):
#     '''
#     task_calculate_movie_ratings(all=False, count=None)
#     task_calculate_movie_ratings.delay(all=False, count=None)
#     task_calculate_movie_ratings.apply_async(
#         kwargs={"all":False, "count":None"},
#         countdown=30
#     )
#     '''

#     qs = Movie.objects.needs_updating() 
#     if all:
#         Movie.objects.all()

#     qs = qs.order_by('rating_last_updated')
#     if isinstance(count, int):
#         qs = qs[:count]

#     for obj in qs:
#         obj.calculate_rating(save=True)

#     return qs.count()
