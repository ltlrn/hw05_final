from django import template

register = template.Library()


@register.filter
def addclass(field, css):
    """Фильтр добавления класса."""
    return field.as_widget(attrs={'class': css})
