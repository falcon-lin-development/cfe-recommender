from typing import Any, Optional
from django.core.management.base import BaseCommand, CommandError, CommandParser
from django.contrib.auth import get_user_model

from cfehome import utils as cfehome_utils
User = get_user_model() # for custom user model

class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "count", 
            nargs="?",
            type=int, 
            default=10,
            help="Number of users to create"
        )
        parser.add_argument(
            "--show-total",
            action="store_true",
            default=False,
        )

    def handle(self, *args: Any, **options: Any):
        count = options.get("count")
        show_total = options.get("show_total")
        profiles = cfehome_utils.get_fake_profiles(
            count=count
        )

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