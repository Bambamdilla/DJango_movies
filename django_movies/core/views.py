# from django.http import HttpResponse
from concurrent.futures._base import LOGGER

from django.shortcuts import render
from django.views.generic import ListView, FormView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django import views
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin

from core.models import Movie, age_limit_choices
from core.forms import MovieForm
import logging

# class MovieCreateView(FormView):
#     template_name = 'form.xhtml'
#     form_class = MovieForm

class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


logging.basicConfig(
    filename='log.txt',
    filemode='w',  # tryb zapisu, jak nie ma pliku, to go stworzy
    level=logging.INFO,  # zapisujemy info z loggingu od najniższego poziomu, najwyżej jest CRITICAL
)

LOGGER = logging.getLogger(__name__)
# bez name'a pewnie też by zadziałał


class MovieCreateView(StaffRequiredMixin, LoginRequiredMixin, CreateView):
    # title = 'Add Movie' # niepotrzebne, przydaje się przy bazie danych
    template_name = 'form.xhtml'
    form_class = MovieForm
    success_url = reverse_lazy('core:movie_list')

    def form_invalid(self, form):
        LOGGER.warning('Invalid data provided')
        return super().form_invalid(form)

    def post(self, request, *args, **kwargs):
        result = super().post(request, *args, **kwargs)
        # print(request.__dict__)
        # dict pokazuje szczegóły naszego działania, wywala mnóstwo danych, do których można się dostać
        # interesuje nas Query Dict, który wyszedł z _post (słownik)
        title = request._post.get('title') # klucz: title, wartość: tytuł filmu
        LOGGER.info(f'Movie {title} has been added to database.')
        return result

        # walrus operator:
        # if title := request._post.get('title'):  # klucz: title, wartość: tytuł filmu
        #     LOGGER.info(f'Movie {title} has been added to database.')
        # return result


class MovieUpdateView(StaffRequiredMixin, LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'form.xhtml'
    model = Movie
    form_class = MovieForm
    # mając form_class odwołujemy się do konkretnej klasy, ale i tak musimy odwoływać się do modelu
    success_url = reverse_lazy('core:movie_list')

    def form_invalid(self, form):
        LOGGER.warning('Invalid data provided')
        return super().form_invalid(form)


class MovieDeleteView(StaffRequiredMixin, LoginRequiredMixin, DeleteView):
    template_name = 'movie_confirm_delete.xhtml'
    model = Movie
    success_url = reverse_lazy('core:movie_list')

    def test_func(self):
        super().test_func() # test logiczny, który zatrzymuje funkcję, gdy wyjdzie False
        return self.request.user.is_superuser
    # dodatkowa funkcja dodająca sprawdzanie, czy użytkownik jest także superuserem


class MovieListView(ListView):
    template_name = 'movie_list.xhtml'
    model = Movie

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['age_limit'] = age_limit_choices
        return context

class MovieDetailView(DetailView):
    template_name = 'movie_detail.xhtml'
    model = Movie


class IndexView(MovieListView):
    template_name = 'movie_list.xhtml'
    model = Movie


class MovieView(ListView):
    template_name = 'movies.xhtml'
    # nazwa templatki w htmlu
    model = Movie
    # model = Movie to nawiązanie, do jakiego modelu w models.py nawiązujemy

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
    LOGGER.info('\nWreszcie coś działa')
    return render(
        request,
        template_name='hello.xhtml',
        context={'adjectives': ['beautiful', 'cruel', 'wonderful']},
    )
    # return HttpResponse('Hello world!')
