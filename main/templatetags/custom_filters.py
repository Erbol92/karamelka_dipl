import json
from django import template
from main.models import Bisquit
register = template.Library()

@register.filter
def get_bisquit(value):
    bisq = Bisquit.objects.get(id=value)
    return bisq

@register.filter
def index(lst, item):
    """Возвращает элемент списка по индексу."""
    try:
        return lst.index(item)
    except ValueError:
        return -1  # Возвращаем -1, если элемент не найден