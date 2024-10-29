from django.shortcuts import render, redirect
from .models import *
from user_manager.models import UserProxy
from django.contrib import messages
from django.http import JsonResponse
# Create your views here.


def home(request):
    object_list = Products.objects.all()
    context = {
        'title': 'главная',
        'object_list': object_list,
    }
    return render(request, 'main/templates/home.html', context=context)

def product_detail(request, pk:int, name:str):
    object = Products.objects.get(id=pk)
    context = {
        'title': object.name_product,
        'object': object,
    }
    return render(request, 'main/templates/product_detail.html', context=context)

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
    bisquits = Bisquit.objects.all()
    fillings = Filling.objects.all()
    data = request.POST or None
    print(data)
    context = {
        'bisquits':bisquits,
        'fillings':fillings,
        'title': 'конструктор',
    }
    return render(request, 'main/templates/constructor_2.html', context=context)

def get_bisquit_description(request, bisquit_id):
    try:
        bisquit = Bisquit.objects.get(pk=bisquit_id)
        print(bisquit)
        return JsonResponse({'description': bisquit.descrition})
    except Bisquit.DoesNotExist:
        return JsonResponse({'description': ''})
    
def cart_view(request):
    context ={
        'title':'корзины',
        'user' : UserProxy.objects.get(pk=request.user.pk)
    }
    return render(request, 'main/templates/cart.html', context=context)

def add_to_cart(request,product_id:int):
    user = UserProxy.objects.get(id=request.user.id)
    product = Products.objects.get(id=product_id)
    messages.success(request, user.add_cart(product=product))
    return redirect(request.META.get('HTTP_REFERER'))

def del_cart(request):
    request.user.carts.all().delete()
    messages.success(request, 'Ваша корзина очищена')
    return redirect('/main')

def del_from_cart(request,cart_id:int):
    messages.success(request, Cart.objects.get(id=cart_id).remove_from_cart())
    return redirect('/main/cart_view/')

def add_quant_cart(request,cart_id:int):
    messages.success(request, Cart.objects.get(id=cart_id).add_quant_to_cart())
    return redirect('/main/cart_view/')
