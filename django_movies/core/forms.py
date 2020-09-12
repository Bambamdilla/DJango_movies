from django import forms
import re
from datetime import date

from core.models import Genre, Movie
from django.core.exceptions import ValidationError


def capitalized_validator(value):
    if value[0].islower():
        raise ValidationError('Value must be capitalized.')


class PastMonthField:
    def validate(self, value):
        super().validate(value)
        if value >= date.today():
            raise ValidationError('Only past dates allowed here.')

    def clean(self, value):
        result = super().clean(value)
        return date(year=result.year, month=result.month, day=1)

class MovieForm(forms.Form):
    title = forms.CharField(max_length=100)
    rating = forms.IntegerField(min_value=1, max_value=10)
    released = PastMonthField()
    description = forms.CharField(widget=forms.Textarea, required=False)
    genre = forms.ModelChoiceField(queryset=Genre.objects.all())

    # director = forms.ForeignKey(Movie.Director, null=True, on_delete=models.SET_NULL)
    # countries = forms.ModelMultipleChoiceField(Movie.Country, related_name='movies')

    def clean_description(self): # clean_<fieldname>
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
