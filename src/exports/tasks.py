from celery import shared_task

from . import utils as export_utils

@shared_task(name="export_rating_dataset_task")
def export_rating_dataset_task():
    export_utils.generate_rating_dataset(to_csv=True)


@shared_task(name="export_movie_dataset_task")
def export_movie_dataset_task():
    export_utils.generate_movie_dataset(to_csv=True)