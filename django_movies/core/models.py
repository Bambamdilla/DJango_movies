from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


# Tworząc na modelu działamy na bazie danych.
# Obiekt tworzymy przez migrację z modelu
# Create your models here.

class Genre(models.Model):
    name = models.CharField(max_length=20, unique=True)
    limit_1 = 3
    limit_2 = 7
    limit_3 = 13
    limit_4 = 18
    limit_5 = 21
    age_limit_choices = [
        (limit_1, 3),
        (limit_2, 7),
        (limit_3, 13),
        (limit_4, 18),
        (limit_5, 21),
    ]
    age_limit = models.IntegerField(choices=age_limit_choices, default=limit_1)

    # age_limit = models.IntegerField(default=3, validators=[MaxValueValidator(21)])
    # alternatywny sposób, wpisując z ręki

    def __str__(self):
        return self.name

class Director(models.Model):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.name} {self.surname}"

class Movie(models.Model):
    title = models.CharField(max_length=120)
    rating = models.IntegerField(
        null=True, validators=[MaxValueValidator(10), MinValueValidator(1)]
    )
    # to działa do formularzy, nie do bazy danych
    released = models.DateField(null=True)
    description = models.TextField(null=True, blank=True)
    # null jest do rekordu w bazie danych, blank do formularzy usera
    created = models.DateTimeField(auto_now_add=True)
    # dodaje przy nowym obiekcie czas stworzenia
    genre = models.ForeignKey(Genre, null=True, on_delete=models.SET_NULL)
    director = models.ForeignKey(Director, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.title} from {self.released}"



