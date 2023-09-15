from django.contrib import admin

# Register your models here.
from .models import Movie

class MovieAdmin(admin.ModelAdmin):
    list_display = [
        
        "__str__",
        "id",
        "idx",
        "rating_count", 
        "rating_avg"
        # "rating_last_updated",
    ]
    readonly_fields = [
        'id', 
        "idx",
        "rating_avg", 
        "rating_count", 
        # "rating_avg_display"
    ]
    search_fields = ['id']

admin.site.register(Movie, MovieAdmin)