# from django.http import HttpResponse
from django import views
from django.shortcuts import render
from django.views.generic import ListView, FormView

from core.models import Movie, age_limit_choices
from core.forms import MovieForm


class MovieCreateView(FormView):
    template_name = 'form.xhtml'
    form_class = MovieForm


class MovieView(ListView):
    template_name = 'movies.xhtml'
    model = Movie

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['age_limit'] = age_limit_choices
        return context

    # extra_context = {'movies': Movie.objects.all()}
    # zamiast model = Movie

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
