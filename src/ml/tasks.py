from celery import shared_task
from movies.models import Movie
from profiles import utils as profile_utils
from . import utils as ml_utils

@shared_task
def train_surprise_model_task():
    ml_utils.train_surprise_model()


@shared_task
def batch_user_prediction_task(start_page=0, offset=250, max_pages=1000):
    model = ml_utils.load_model()
    end_page = start_page+offset
    recent_user_ids = profile_utils.get_recent_users()
    movie_ids = Movie.objects.all().popular() \
        .values_list("id", flat=True)[start_page:end_page]

    for movie_id in movie_ids:
        for user_id in recent_user_ids:
            pred = model.predict(uid=user_id, iid=movie_id).est
            print(user_id, movie_id, pred)
            # ml_utils.save_prediction(user_id, movie_id, pred)   

    if end_page < max_pages:
        return batch_user_prediction_task(start_page=end_page-1)
    


@shared_task
def batch_update_user_prediction_task(user_id=1,start_page=0, offset=250, max_pages=100_000):
    model = ml_utils.load_model()
    end_page = start_page+offset
    recent_user_ids = [user_id]
    movie_ids = Movie.objects.all().popular(reverse=True) \
        .values_list("id", flat=True)[start_page:end_page]

    for movie_id in movie_ids:
        for user_id in recent_user_ids:
            pred = model.predict(uid=user_id, iid=movie_id).est
            print(user_id, movie_id, pred)
            # ml_utils.save_prediction(user_id, movie_id, pred)   

    if end_page < max_pages:
        return batch_update_user_prediction_task(user_id=user_id, start_page=end_page-1)