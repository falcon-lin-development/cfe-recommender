from django.db import models
from django.utils import timezone

import uuid
import pathlib

from . import storages as export_storages

def export_file_handler(instance, filename):
    today = timezone.now().strftime('%Y-%m-%d')
    fpath = pathlib.Path(filename)
    ext = fpath.suffix # .csv
    dtype = instance.type
    if hasattr(instance, "id"):
        new_fname = f"{instance.id}{ext}"
    else:
        new_fname = f"{uuid.uuid4()}{ext}"
    return f"exports/{dtype}/{today}/{new_fname}"


class ExportDataType(models.TextChoices):
    RATINGS = "ratings", "Ratings"
    MOVIES = "movies", "Movies"
    # MODELS = "models", "Models"


class Export(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(upload_to=export_file_handler, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    type = models.CharField(
        max_length=255, 
        choices=ExportDataType.choices, 
        default=ExportDataType.RATINGS
    )
    latest = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.file}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.latest and self.file:
            file = self.file
            dtype = self.type
            ext = pathlib.Path(file.name).suffix
            path = f"exports/{dtype}/lastest{ext}"
            export_storages.save(path, file, overwrite=True)
            qs = Export.objects.filter(
                type=dtype, latest=True).exclude(id=self.id)
            qs.update(latest=False)