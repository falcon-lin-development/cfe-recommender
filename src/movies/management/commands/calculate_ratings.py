from typing import Any, Optional
from django.core.management.base import BaseCommand, CommandError, CommandParser
from django.contrib.auth import get_user_model

from cfehome import utils as cfehome_utils
from ratings.tasks import task_update_movie_ratings
from ratings.models import Rating
User = get_user_model() # for custom user model

class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any):
        task_update_movie_ratings()