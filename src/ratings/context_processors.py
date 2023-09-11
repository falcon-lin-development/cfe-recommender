
from .models import RatingChoices
def rating_choices(request):
    return {
        "rating_choices": RatingChoices.values
    }