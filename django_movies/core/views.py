# from django.http import HttpResponse
from django import views
from django.shortcuts import render
from django.views.generic import TemplateView

from core.models import Movie, age_limit_choices


class MovieView(TemplateView):
    template_name = 'movies.xhtml'
    extra_context = {'movies': Movie.objects.all()}
    # def get(self, request):
    #     return render(
    #         request,
    #         template_name='movies.xhtml',
    #         context={'movies': Movie.objects.all()}
    #     )


# Create your views here.
def movies(request):
    return render(
        request,
        template_name='movies.xhtml',
        context={'movies': Movie.objects.all(), 'age_limit': age_limit_choices},
    )


def hello(request):
    return render(
        request,
        template_name='hello.xhtml',
        context={'adjectives': ['beautiful', 'cruel', 'wonderful']},
    )
    # return HttpResponse('Hello world!')
