from typing import Any, Optional
from django.core.management.base import BaseCommand, CommandError, CommandParser
from django.contrib.auth import get_user_model

from cfehome import utils as cfehome_utils

from movies.models import Movie
User = get_user_model() # for custom user model

class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("count", nargs="?", type=int, default=10)
        parser.add_argument("--movies", action="store_true", default=False,)
        parser.add_argument("--users", action="store_true", default=False,)
        parser.add_argument("--show-total", action="store_true", default=False,)

    def handle(self, *args: Any, **options: Any):
        count = options.get("count")
        show_total = options.get("show_total")
        load_movies = options.get("movies")
        generate_users = options.get("users")

        if load_movies:
            movies_dataset = cfehome_utils.load_movie_data(limit=count)
            movies_new = [Movie(**x) for x in movies_dataset]
            movies_bulk = Movie.objects.bulk_create(movies_new, ignore_conflicts=True)

            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully created {len(movies_bulk)} movies"
                )
            )
            if show_total:
                total_movies = Movie.objects.count()
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Total movies: {total_movies}"
                    )
                )
        
        if generate_users:
            profiles = cfehome_utils.get_fake_profiles(count=count)

            new_users = []
            for profile in profiles:
                user = User(**profile)
                new_users.append(user)
            
            user_bulk = User.objects.bulk_create(new_users, ignore_conflicts=True)

            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully created {len(user_bulk)} users"
                )
            )
            if show_total:
                total_users = User.objects.count()
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Total users: {total_users}"
                    )
                )