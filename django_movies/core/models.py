from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from model_utils import Choices


# Tworząc na modelu działamy na bazie danych.
# Obiekt tworzymy przez migrację z modelu
# Create your models here.

age_limit_choices = Choices(
        (0, 'kids', 'dzieci'),
        (1, 'teens', 'nastolatki'),
        (2, 'adults', 'dorośli'),
    )

class Genre(models.Model):
    name = models.CharField(max_length=20, unique=True)

    age_limit = models.IntegerField(choices=age_limit_choices, default=0)

    # age_limit = models.IntegerField(default=3, validators=[MaxValueValidator(21)])
    # alternatywny sposób, wpisując z ręki

    def __str__(self):
        return self.name


class Director(models.Model):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)

    class Meta:
        unique_together = ('name', 'surname')
        # Django wie, że unique_together to wbudowana zmienna

    def __str__(self):
        return f"{self.name} {self.surname}"


class Country(models.Model):
    name = models.CharField(max_length=30, unique=True)

    class Meta:
        ordering = (
            'name',
        )

    def __str__(self):
        return f"{self.name}"


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
    countries = models.ManyToManyField(Country, related_name='movies')

    class Meta:
        unique_together = ('title', 'released', 'director')

    def __str__(self):
        return f"{self.title} from {self.released}"
