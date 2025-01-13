import json
from django import template
from main.models import Bisquit
register = template.Library()

@register.filter
def get_bisquit(value):
    bisq = Bisquit.objects.get(id=value)
    return bisq