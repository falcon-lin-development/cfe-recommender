from django.conf import settings
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models.query import QuerySet

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

class RatingManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return RatingQuerySet(self.model, using=self._db)

    def avg(self):
        self.get_queryset().avg()

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField(null=True, blank=True, choices=RatingChoices.choices)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField() # dont work on UUID
    content_object = GenericForeignKey("content_type", "object_id")
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = RatingManager() # Rating.objects.all().avg()  # Rating.objects.avg()