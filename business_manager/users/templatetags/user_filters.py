from django.forms.boundfield import BoundField
from django.template.library import Library

register = Library()


@register.filter
def addclass(field: BoundField, css: str):
    """Добавление CSS-класса тегу"""
    return field.as_widget(attrs={"class": css})
