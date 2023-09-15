from celery import shared_task
from movies.models import Movie
from profiles import utils as profile_utils
from . import utils as ml_utils
from django.apps import apps
from django.contrib.contenttypes.models import ContentType

@shared_task
def train_surprise_model_task():
    ml_utils.train_surprise_model()


@shared_task
def batch_users_prediction_task(user_ids = None, start_page=0, offset=250, max_pages=1000):
    model = ml_utils.load_model()
    Suggestion = apps.get_model("suggestions", "Suggestion")
    ctype = ContentType.objects.get(app_label="movies", model="movie")

    end_page = start_page+offset
    if user_ids is None:
        user_ids = profile_utils.get_recent_users()
    
    movie_ids = Movie.objects.all().popular() \
        .values_list("id", flat=True)[start_page:end_page]

    new_suggestions = []
    for movie_id in movie_ids:
        for user_id in user_ids:
            pred = model.predict(uid=user_id, iid=movie_id).est
            # ml_utils.save_prediction(user_id, movie_id, pred)   
            data ={
                "user_id": user_id,
                "object_id": movie_id,
                "value": pred,
                "content_type": ctype, 
            }
            new_suggestions.append(Suggestion(**data))
    Suggestion.objects.bulk_create(new_suggestions, ignore_conflicts=True)

    if end_page < max_pages:
        return batch_users_prediction_task(start_page=end_page-1)
    


@shared_task
def batch_single_user_prediction_task(user_id=1,start_page=0, offset=250, max_pages=100_000):
    return batch_users_prediction_task(user_ids=[user_id], start_page=start_page, offset=offset, max_pages=max_pages)