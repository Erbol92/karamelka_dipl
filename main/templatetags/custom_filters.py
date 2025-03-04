import json
from django import template
register = template.Library()



@register.filter
def get_size(lst:dict, item:str):
    if lst:
        return lst[item]
