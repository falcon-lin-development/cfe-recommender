from django.contrib import admin

# Register your models here.
from .models import Rating

class RatingAdmin(admin.ModelAdmin):
    raw_id_fields = ["user"]
    readonly_fields = ["content_object"]

admin.site.register(Rating, RatingAdmin)