from django.contrib import admin

# Register your models here.
from .models import Movie

class MovieAdmin(admin.ModelAdmin):
    list_display = [
        
        "__str__",
        "rating_count", 
        "rating_last_updated", "rating_avg"
    ]
    readonly_fields = [
        'id', 
        "rating_avg", 
        "rating_count", 
        "rating_avg_display"
    ]
    search_fields = ['id']

admin.site.register(Movie, MovieAdmin)