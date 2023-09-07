from typing import Any, Optional
from django.core.management.base import BaseCommand, CommandError, CommandParser
from django.contrib.auth import get_user_model

from cfehome import utils as cfehome_utils
from ratings.tasks import generate_fake_reviews
from ratings.models import Rating
User = get_user_model() # for custom user model

class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("count", nargs="?", type=int, default=10)
        parser.add_argument("--users", default=1000, type=int,)
        parser.add_argument("--show-total", action="store_true", default=False,)

    def handle(self, *args: Any, **options: Any):
        count = options.get("count")
        show_total = options.get("show_total")
        user_count = options.get("users")
        new_ratings = generate_fake_reviews(count=count, users=user_count)
        total_ratings = len(new_ratings)
        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully created {total_ratings} ratings"
            )
        )
        if show_total:
            qs = Rating.objects.all()
            self.stdout.write(
                self.style.SUCCESS(
                    f"Total ratings: {qs.count()}"
                )
            )