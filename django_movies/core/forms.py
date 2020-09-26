from django import forms
import re
from datetime import date

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Layout, Row, Submit
from core.models import Genre, Movie
from django.core.exceptions import ValidationError


def capitalized_validator(value):
    if value[0].islower():
        raise ValidationError('Value must be capitalized.')


class PastMonthField(forms.DateField):
    def validate(self, value):
        super().validate(value)
        if value >= date.today():
            raise ValidationError('Only past dates allowed here.')

    def clean(self, value):
        result = super().clean(value)
        return date(year=result.year, month=result.month, day=1)


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        # fields = '__all__' # be explicit!, poniższe rozwiązanie jeszcze lepsze, nawet jak wypisujemy wszystko
        fields = (
            'title',
            'rating',
            'released',
            'description',
            'genre',
            'director',
            'countries',
        )

    title = forms.CharField(validators=[capitalized_validator])
    rating = forms.IntegerField(min_value=1, max_value=10)
    released = PastMonthField()
    # director = forms.ForeignKey(Movie.Director, null=True, on_delete=models.SET_NULL)
    # countries = forms.ModelMultipleChoiceField(Movie.Country, related_name='movies')
    # niepotrzebne, jeśli nie zmieniamy ich w formularzu


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper() # form crispy_forms.helper
        self.helper.layout = Layout(
            'title',
            Row(Column('genre'), Column('rating'), Column('released')),
            'director',
            'description',
            'countries',
            Submit('submit', 'Submit'),
        )

    def clean_description(self):  # clean_<fieldname>
        initial = self.cleaned_data['description']
        sentences = re.sub(r'\s*\.\s*', '.', initial).split('.')
        cleaned = '. '.join(sentence.capitalize() for sentence in sentences)
        return cleaned

    def clean(self):
        result = super().clean()
        # clean jest metodą z django
        if result['genre'].name == 'Komedia' and result['rating'] > 5:
            raise ValidationError('The best comedy is worth a 5.')
        return result
