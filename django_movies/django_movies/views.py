from core.views import MovieListView


class IndexView(MovieListView):
    title = 'Welcome to Django Movie'
    template_name = 'index.xhtml'
