from django.contrib import admin
from core.models import Movie, Genre, Director

# Register your models here.
admin.site.register(Genre)
admin.site.register(Movie)
admin.site.register(Director)