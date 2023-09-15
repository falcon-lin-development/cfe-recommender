from django.apps import apps
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models.query import QuerySet
from django.utils import timezone


# Create your models here.
User = settings.AUTH_USER_MODEL

class RatingChoices(models.IntegerChoices):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    __empty__ = "Rate this"

class RatingQuerySet(models.QuerySet):
    def avg(self):
        return self.aggregate(average=models.Avg("value"))["average"]

    def movies(self):
        Movie = apps.get_model("movies", "Movie")
        ctype = ContentType.objects.get_for_model(Movie)
        return self.filter(content_type=ctype, active=True)

    def as_object_dict(self, object_ids=[]):
        qs = self.filter(
            # movie__in=self.queryset
            object_id__in=object_ids,
        )
        return {f"{x.object_id}": x.value for x in qs}

class RatingManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return RatingQuerySet(self.model, using=self._db)

    def movies(self):
        return self.get_queryset().movies()

    def avg(self):
        self.get_queryset().avg()

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField(null=True, blank=True, choices=RatingChoices.choices)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField() # dont work on UUID
    content_object = GenericForeignKey("content_type", "object_id")
    active = models.BooleanField(default=True)
    active_update_timestamp = models.DateTimeField(
        auto_now=False, auto_now_add=False, blank=True, null=True
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = RatingManager() # Rating.objects.all().avg()  # Rating.objects.avg()


    class Meta:
        ordering = ["-timestamp"]


def rateing_post_save(sender, instance, created, *args, **kwargs):
    if created:
        Suggestion = apps.get_model("suggestions", "Suggestion")

        _id = instance.id
        if instance.active:
            qs = Rating.objects.filter(
                content_type=instance.content_type,
                object_id=instance.object_id, 
                user=instance.user
            ).exclude(id=_id, active=True)
            if qs.exists():
                qs = qs.exclude(active_update_timestamp__isnull=False)
                qs.update(active=False, active_update_timestamp=timezone.now())
            # qs.delete()
            suggestion_qs = Suggestion.objects.filter(
                content_type=instance.content_type,
                object_id=instance.object_id,
                user=instance.user,
                did_rate=False
            )
            if suggestion_qs.exists():
                suggestion_qs.update(
                    did_rate=True,
                    did_rate_timestamp=timezone.now(),
                    rating_value=instance.value
                )


post_save.connect(rateing_post_save, sender=Rating)