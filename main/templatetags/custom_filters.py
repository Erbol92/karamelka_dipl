import json
from django import template

register = template.Library()

translations = {
    "decoration": "Украшение",
    "sprinkles": "Посыпка",
    "shape": "Форма",
    "rectangle": "Прямоугольник",
    "circle": "Круг",
    "layers": "Слои",
    "circle": "окружность",
    "rectangle": "прямоугольник",
    "diameter": "диаметр",
    "height": "высота",
    "width": "ширина",
    "length": "длина",
}


@register.filter
def get_size(lst: dict, item: str):
    if lst:
        return lst[item]


@register.filter
def discount(price: int):
    return price * 0.9


@register.filter
def translate(name: str):
    print(name)
    return translations[name]
