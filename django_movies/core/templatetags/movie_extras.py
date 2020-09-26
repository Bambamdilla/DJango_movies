from django.template import Library
from django.utils.html import escape
# escape parsuje dane do widoku html
from django.utils.safestring import SafeString
# SafeString parsuje dane do widoku html

register = Library()


@register.simple_tag
def movie_format(movie, short=False):
    if short:
        return f'{movie.title}'
    return f'{movie.title} ({movie.released.year}) - {movie.genre}'


@register.filter
def attr_as_p(obj, attrname):
    label = escape(attrname.capitalize())
    # nazwa atrybutu - tytuł
    value = escape(getattr(obj, attrname))
    # nazwa wartości - tytuł
    return SafeString(f'<p><strong>{label}:</strong> {value}</p>')
