from django.shortcuts import render
from .models import *
# Create your views here.


def home(request):
    object_list = Products.objects.all()
    context = {
        'title': 'главная',
        'object_list': object_list,
    }
    return render(request, 'main/templates/home.html', context=context)


def category_page(request, category):
    object_list = Products.objects.filter(category__slug=category)
    context = {
        'title': 'главная',
        'object_list': object_list,
    }
    return render(request, 'main/templates/home.html', context=context)


def main_page_objects(request):
    category_list = CategoryProduct.objects.all()
    context = {'category_list': category_list, }
    return context


def constructor(request):
    context = {
        'title': 'конструктор',
    }
    return render(request, 'main/templates/constructor.html', context=context)
