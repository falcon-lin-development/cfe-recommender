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
    active_update_timestamp = models.DateTimeField(
        auto_now=False, auto_now_add=False, blank=True, null=True
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = RatingManager() # Rating.objects.all().avg()  # Rating.objects.avg()


    class Meta:
        ordering = ["-timestamp"]


def rateing_post_save(sender, instance, created, *args, **kwargs):
    if created:
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

post_save.connect(rateing_post_save, sender=Rating)