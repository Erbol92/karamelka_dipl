from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from user_manager.models import UserProxy
from django.contrib import messages
from django.http import JsonResponse
import json
import uuid
from .forms import CommentForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
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
    comments = object.comments.filter(parent__isnull=True,moderated=True)
    form = CommentForm(request.POST or None)
    if request.user.is_authenticated:
        if object.id in set(request.user.orders.all().values_list('product',flat=True)):
            if form.is_valid():
                parent_id = request.POST.get('parent_id')
                comment = form.save(commit=False)
                comment.product = object
                comment.user = request.user
                if parent_id:
                    comment.parent = get_object_or_404(Comment, id=parent_id)
                comment.save()
                return redirect('product_detail', pk=object.id, name=object.name_product)
        else:
            messages.success(request, 'Вы не заказывали данный продукт')

    context = {
        'title': object.name_product,
        'object': object,
        'form':form,
        'comments':comments,
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
    context = {
        'bisquits':bisquits,
        'fillings':fillings,
        'title': 'конструктор',
    }
    return render(request, 'main/templates/constructor_2.html', context=context)


def constructor_ajax(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Загружаем JSON-данные
            # Обработка данных
            print(data)  # Выводим данные в консоль (или обрабатываем их)
            CartConstructor.objects.create(user=request.user,uniq_id=uuid.uuid4().hex,data = data)
            print('ok')
            
            return JsonResponse({'status': 'success', 'data': data})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Only POST requests are allowed'}, status=405)

def get_bisquit_description(request, bisquit_id):
    try:
        bisquit = Bisquit.objects.get(pk=bisquit_id)
        print(bisquit)
        return JsonResponse({'description': bisquit.descrition})
    except Bisquit.DoesNotExist:
        return JsonResponse({'description': ''})

@login_required(login_url=reverse_lazy('auth'))    
def cart_view(request):
    context ={
        'title':'корзины',
        'user' : UserProxy.objects.get(pk=request.user.pk),
        'orders': request.user.orders.all()
    }
    data = request.POST or None
    if data:
        print(data)
        select_cart = data.getlist('select_cart')
        select_consrt_cart = data.getlist('select_consrt_cart')
        place,pay = {},{}
        delivery = data.get('delivery')
        if delivery:
            place['delivery'] = delivery
            if delivery =='доставка':
                address = data.get('address')
                print(address)
                if address:
                    place['address'] = address
                    
            place = json.dumps(place, indent=4)
            print(place)
        payment = data.get('payment')
        if payment:
            pay['payment'] = payment
            card_number = data.get('cardNumber')
            if payment == 'безналичная':
                expiry_date= data.get('expiryDate')
                cvv = data.get('cvv')
                # pay['payment'] = {payment:{'card_number':card_number,
                #                         'expiry_date':expiry_date,
                #                         'cvv':cvv
                #                         }
                #                 }
            pay = json.dumps(pay, indent=4)
        if select_cart:
            orders = []
            for cart_id in select_cart:
                cart = Cart.objects.get(id=int(cart_id))
                orders.append(Order(user=request.user,product=cart.product,quantity=cart.quantity,place=place,payment=pay))
            Order.objects.bulk_create(orders)
            Cart.objects.filter(id__in=select_cart).delete()
        
        if select_consrt_cart:
            orders = []
            for cart_id in select_consrt_cart:
                cart = CartConstructor.objects.get(id=int(cart_id))
                orders.append(Order(user=request.user,consrt=cart.data,quantity=cart.quantity,place=place,payment=pay))
            Order.objects.bulk_create(orders)
            CartConstructor.objects.filter(id__in=select_consrt_cart).delete()
    return render(request, 'main/templates/cart.html', context=context)

@login_required(login_url=reverse_lazy('auth'))
def add_to_cart(request,product_id:int):
    user = UserProxy.objects.get(id=request.user.id)
    product = Products.objects.get(id=product_id)
    messages.success(request, user.add_cart(product=product))
    return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url=reverse_lazy('auth'))
def del_cart(request):
    request.user.carts.all().delete()
    request.user.carts_constr.all().delete()
    messages.success(request, 'Ваша корзина очищена')
    return redirect('/main')

@login_required(login_url=reverse_lazy('auth'))
def del_from_cart(request,type:str,cart_id:int):
    match type:
        case 'constr':
            cart = CartConstructor.objects.get(id=cart_id)
        case 'prod':
            cart = Cart.objects.get(id=cart_id)
    messages.success(request, cart.remove_from_cart())
    return redirect('/main/cart_view/')

@login_required(login_url=reverse_lazy('auth'))
def add_quant_cart(request,type:str,cart_id:int):
    match type:
        case 'constr':
            cart = CartConstructor.objects.get(id=cart_id)
        case 'prod':
            cart = Cart.objects.get(id=cart_id)
    messages.success(request, cart.add_quant_to_cart())
    return redirect('/main/cart_view/')

