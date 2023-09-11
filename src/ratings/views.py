from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
from django.views.decorators.http import require_http_methods
from .models import Rating

# Create your views here.
@require_http_methods(["POST"])
def rate_movie_view(request):
    if not request.htmx:
        return HttpResponse("Not allowed", status=400)
    object_id = request.POST.get('object_id')   
    rating_value = request.POST.get('rating_value') 
    if object_id is None or rating_value is None:
        response =  HttpResponse("Skipping", status=200)
        response['HX-Trigger'] = 'did-skip-movie'
        return response
    user = request.user
    message = "you must <a href='/accounts/login'>login</a> to rate movies"
    if user.is_authenticated:
        message = "<span class='bg-danger text-light px-3 py-1 rounded'>An error occured.</span>"
        ctype = ContentType.objects.get(app_label='movies', model='movie')
        rating_obj = Rating.objects.create(
            user=user,
            content_type=ctype,
            object_id=object_id,
            value=rating_value,
        )
        if rating_obj.content_object is not None:
            message = "<span class='bg-success text-light px-3 py-1 rounded'>Thank you for rating.</span>"
            response =  HttpResponse("rating", status=200)
            response['HX-Trigger-After-Settle'] = 'did-rate-movie'
            return response
   
    return HttpResponse(message, status=200)