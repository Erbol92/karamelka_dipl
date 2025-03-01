from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Max
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

from user_manager.models import UserProxy
from .forms import CommentForm, DecorationFormSet
from .gigachat import push_and_get_photo
from .models import *


# Create your views here.

def home(request):
    object_list = Products.objects.all()
    context = {
        'title': 'главная',
        'object_list': object_list,
    }
    return render(request, 'main/templates/home.html', context=context)


def product_detail(request, pk: int, name: str):
    object = Products.objects.get(id=pk)
    comments = object.comments.filter(parent__isnull=True, moderated=True)
    form = CommentForm(request.POST or None)
    if request.user.is_authenticated:
        if object.id in set(request.user.orders.all().values_list('product', flat=True)):
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
        'form': form,
        'comments': comments,
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
    text = ('Сделай картинку торта: \n'
            )
    bisquit, filling, support, layers, shape = '', '', '', '', ''
    shape_ru = shape
    bisquits = Bisquit.objects.all()
    fillings = Filling.objects.all()
    sprinkles = Sprinkles.objects.all()
    formset = DecorationFormSet(request.POST or None)
    with open('main/LayerSize.json') as f:
        sizes = json.load(f)
    context = {
        'bisquits': bisquits,
        'fillings': fillings,
        'sizes': sizes,
        'title': 'конструктор',
        'sprinkleses': sprinkles,
        'formset': formset,
    }
    if request.method == 'POST':
        data = request.POST
        if data.get('action') == 'generate':
            if data.get('biscuit', None):
                bisquit = Bisquit.objects.get(id=data['biscuit'])
                text += f'Основа: {bisquit.title}\n'

            if data.get('filling', None):
                filling = Filling.objects.get(id=data['filling'])
                text += f'Начинка: {filling.title} \n'

            if formset.is_valid():
                text += 'Украшения:\n'
                for form in formset:
                    decoration = form.cleaned_data.get('decoration')
                    quantity = form.cleaned_data.get('quantity')
                    if decoration and quantity:
                        text += f'{decoration.title}: {quantity} штук\n'

            if data.getlist('sprinkles'):
                text += 'Посыпка: '
                sprinks = Sprinkles.objects.filter(id__in=data.getlist('sprinkles'))
                text += ', '.join(sprink.title for sprink in sprinks)
                text += '\n'

            if data.get('shape'):
                shape = data['shape']
                match shape:
                    case 'rectangle':
                        shape_ru = 'прямоугольная'
                    case 'circle':
                        shape_ru = 'круг'
                text += f'форма уровней {shape_ru} \n'

            if data.get('layers'):
                layers = int(data['layers'])
                text += f'Количество уровней: {layers}  \n'
                for i in range(1, layers + 1):
                    size = data.get(f"size-{i}").split('x')
                    if shape == 'rectangle':
                        text += f'уровень {i}  длина {size[0]} см. ширина {size[1]} см. высота {size[2]} см.\n'
                    if shape == 'circle':
                        text += f'уровень {i} диаметр {size[0]} см. высота {size[1]} см.\n'
                context.update({'text': text, 'image_url': '/media/fl.jpg'})
                push_and_get_photo(text)
                return render(request, 'main/templates/constructor.html',
                              context=context)

    return render(request, 'main/templates/constructor.html', context=context)


def preview_constructor(request):
    print(request.POST)
    if request.method == 'POST':
        data = request.POST
        bisquit = Bisquit.objects.get(id=data['biscuit'])
        filling = Filling.objects.get(id=data['filling'])
        shape = data['shape']
        support = 'длина ширина высота' if shape == 'rectangle' else 'диаметр*высота'
        layers = int(data['layers'])
        # 'layers': ['2'], 'biscuit': ['1'], 'filling': ['1'], 'shape': ['rectangle'], 'size-1': ['40x40x20'], 'size-2': ['30x20x10']}
        text = ('Представь что ты визуализатор \n'
                'Сделай картинку торта: \n'
                f'Торт состоит из {layers} уровней \n'
                f'формы уровней {shape} \n'
                f'бисквит {bisquit.title}, начинка {filling.title} \n'
                )
        for i in range(1, layers + 1):
            text += f'уровень {i} размером {data.get(f"size-{i}")} {support}\n'
        text += 'учитывай указанные размеры уровней \n'
        text += 'без обозначения размеров на картинке \n'
        image_url = push_and_get_photo(text)
        print(image_url)
        context = {
            'image_url': image_url,
        }
    return render(request, 'main/templates/constructor.html', context=context)


@login_required(login_url=reverse_lazy('auth'))
def cart_view(request):
    context = {
        'title': 'корзины',
        'user': UserProxy.objects.get(pk=request.user.pk),
        'orders': request.user.orders.all()
    }
    data = request.POST or None
    if data:
        print(data)
        select_cart = data.getlist('select_cart')
        select_consrt_cart = data.getlist('select_consrt_cart')
        place, pay = {}, {}
        delivery = data.get('delivery')
        if delivery:
            place['delivery'] = delivery
            if delivery == 'доставка':
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
                expiry_date = data.get('expiryDate')
                cvv = data.get('cvv')
                # pay['payment'] = {payment:{'card_number':card_number,
                #                         'expiry_date':expiry_date,
                #                         'cvv':cvv
                #                         }
                #                 }
            pay = json.dumps(pay, indent=4)

        # Получаем максимальный номер заказа для текущего пользователя
        max_order_num = Order.objects.filter(user=request.user).aggregate(Max('num_order'))['num_order__max'] or 0
        current_order_num = max_order_num + 1

        if select_cart:
            orders = []
            for cart_id in select_cart:
                cart = Cart.objects.get(id=int(cart_id))
                orders.append(
                    Order(user=request.user, product=cart.product, quantity=cart.quantity, place=place, payment=pay,
                          num_order=current_order_num))
            Order.objects.bulk_create(orders)
            Cart.objects.filter(id__in=select_cart).delete()

        if select_consrt_cart:
            orders = []
            for cart_id in select_consrt_cart:
                cart = CartConstructor.objects.get(id=int(cart_id))
                orders.append(
                    Order(user=request.user, consrt=cart.data, quantity=cart.quantity, place=place, payment=pay,
                          num_order=current_order_num))
            Order.objects.bulk_create(orders)
            CartConstructor.objects.filter(id__in=select_consrt_cart).delete()
        return redirect('cart_view')
    return render(request, 'main/templates/cart.html', context=context)


@login_required(login_url=reverse_lazy('auth'))
def add_to_cart(request, product_id: int):
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
def del_from_cart(request, type: str, cart_id: int):
    match type:
        case 'constr':
            cart = CartConstructor.objects.get(id=cart_id)
        case 'prod':
            cart = Cart.objects.get(id=cart_id)
    messages.success(request, cart.remove_from_cart())
    return redirect('/main/cart_view/')


@login_required(login_url=reverse_lazy('auth'))
def add_quant_cart(request, type: str, cart_id: int):
    match type:
        case 'constr':
            cart = CartConstructor.objects.get(id=cart_id)
        case 'prod':
            cart = Cart.objects.get(id=cart_id)
    messages.success(request, cart.add_quant_to_cart())
    return redirect('/main/cart_view/')
