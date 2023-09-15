from django.contrib import admin

# Register your models here.
from .models import Suggestion

class SuggestionAdmin(admin.ModelAdmin):
    list_display = ["content_object", "user", "value"]
    raw_id_fields = ["user"]
    readonly_fields = ["content_object"]
    search_fields = ["user__username"]

admin.site.register(Suggestion, SuggestionAdmin)