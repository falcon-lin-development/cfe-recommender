from typing import Any, Optional
from django.core.management.base import BaseCommand, CommandError, CommandParser
from django.contrib.auth import get_user_model

from cfehome import utils as cfehome_utils
from movies.tasks import task_calculate_movie_ratings
from ratings.models import Rating
User = get_user_model() # for custom user model

class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("count", nargs="?", type=int, default=1_000)
        parser.add_argument("--all", action="store_true", default=False,)

    def handle(self, *args: Any, **options: Any):
        all = options.get("all")
        count = options.get("count")
        number_of_updated = task_calculate_movie_ratings(all=all, count=count)
        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully calculated ratings: {number_of_updated}"
            )
        )