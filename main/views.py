import math
import time
from django.db.models import Sum
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Max
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import JsonResponse

from user_manager.models import UserProxy
from .forms import CommentForm, DecorationFormSet
from .models import *
from .gigachat import push_and_get_photo


# Create your views here.
def convert_minutes_to_hours_and_minutes(total_minutes):
    hours = total_minutes // 60  # Целочисленное деление для получения часов
    minutes = total_minutes % 60  # Остаток от деления для получения минут
    return hours, minutes


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


def volume_calc(form: str, size: list):
    size = [int(num) for num in size]
    match form:
        case 'rectangle':
            return size[0] * size[1] * size[2]
        case 'circle':
            return 3.14 * size[0] * size[0] * size[1] / 4


def constructor(request):
    text = ''
    bisquit, filling, support, layers, shape = '', '', '', '', ''
    shape_ru = shape
    return_text = ''
    characteristics = {}
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
    decoration_added = False
    if request.method == 'POST':
        data = request.POST
        if data.get('action') == 'order':
            if data.get('biscuit', None):
                bisquit = Bisquit.objects.get(id=data['biscuit'])
                text += f'Основа: {bisquit.title}\n'
                characteristics['bisquit'] = bisquit

            if data.get('filling', None):
                filling = Filling.objects.get(id=data['filling'])
                text += f'Начинка: {filling.title} \n'
                characteristics['filling'] = filling

            if formset.is_valid():
                characteristics['decoration'] = []
                characteristics['decoration_price'] = 0
                for form in formset:
                    decoration = form.cleaned_data.get('decoration')
                    quantity = form.cleaned_data.get('quantity')
                    if decoration and quantity:
                        if not decoration_added:
                            text += 'Украшения:\n'
                            decoration_added = True
                        text += f'{decoration.title}: {quantity} штук\n'
                        characteristics['decoration'].append({decoration: quantity})
                        characteristics['decoration_price'] += decoration.price * quantity

            if data.getlist('sprinkles'):
                characteristics['sprinks_price'] = 0
                text += 'Посыпка: '
                sprinks = Sprinkles.objects.filter(id__in=data.getlist('sprinkles'))
                text += ', '.join(sprink.title for sprink in sprinks)
                characteristics['sprinks'] = sprinks
                characteristics['sprinks_price'] += sum(sprink.price for sprink in sprinks)
                text += '\n'

            if data.get('shape'):
                shape = data['shape']
                match shape:
                    case 'rectangle':
                        shape_ru = 'прямоугольная'
                    case 'circle':
                        shape_ru = 'круг'
                characteristics['shape_ru'] = shape_ru
                text += f'форма уровней {shape_ru} \n'
            if data.get('text_decoration'):
                text_decoration = data.get('text_decoration')
                characteristics['text_decoration'] = text_decoration
                text += f'надпись на торте: {text_decoration}\n'
            if data.get('layers'):
                layers = int(data['layers'])
                match layers:
                    case 1:
                        text += 'одноярусный\n'
                    case 2:
                        text += 'двухъярусный\n'
                    case 3:
                        text += 'трехъярусный\n'
                characteristics['volume'] = 0
                return_text = text
                for i in range(1, layers + 1):
                    size = data.get(f"size-{i}").split('x')

                    if shape == 'rectangle':
                        return_text += f'ярус {i}  длина {size[0]} см. ширина {size[1]} см. высота {size[2]} см.\n'
                        text += f'ярус {i} площадью {2 * (int(size[0]) + int(size[1])) * int(size[2])}\n'
                    if shape == 'circle':
                        return_text += f'ярус {i} диаметр {size[0]} см. высота {size[1]} см.\n'
                        text += f'ярус {i} площадью {3.14 * float(size[0]) * (int(size[1]) + int(size[0]) / 2)}\n'
                    characteristics['volume'] += volume_calc(shape, size)
                characteristics['volume'] /= 10 ** 6
                characteristics['weight'] = math.ceil(characteristics['volume'] * (
                        characteristics['bisquit'].weight + 0.3 * characteristics['filling'].weight))

                characteristics['price'] = characteristics['volume'] * (
                        characteristics['bisquit'].weight * characteristics['bisquit'].price + 0.3 *
                        characteristics['filling'].weight * characteristics['filling'].price)
                characteristics['price'] += characteristics.get('sprinks_price', 0) + characteristics.get(
                    'decoration_price', 0) + 100 if data.get('text_decoration') else 0
                characteristics['price'] = math.ceil(characteristics['price'])
                cook_time = bisquit.cooking_time + filling.cooking_time
                print(cook_time)
                orders_time = Order.objects.filter(state='in_job').aggregate(total=Sum('consrt__cook_time')).get('total')
                print(Order.objects.filter(state='in_job').values_list('consrt__cook_time',flat=True))
                if orders_time:
                    total_cook_time_value = cook_time + orders_time
                else:
                    total_cook_time_value = cook_time
                print(total_cook_time_value)
                CartConstructor.objects.create(user=request.user, quantity=1, price=characteristics['price'],
                                               data=return_text, cook_time=total_cook_time_value)
                return_text += f"масса: {characteristics['weight']} кг.\n"
                return_text += f"цена: {characteristics['price']} руб.\n"
                # push_and_get_photo(text)
                context.update({'text': return_text})
                print(text)


                return render(request, 'main/templates/constructor.html',
                              context=context)
        else:
            print(request.POST)
    return render(request, 'main/templates/constructor.html', context=context)


def preview_constructor(request):
    text = ''
    bisquit, filling, support, layers, shape = '', '', '', '', ''
    shape_ru = shape
    return_text = ''
    characteristics = {}
    decoration_added = False
    formset = DecorationFormSet(request.POST or None)
    if request.method == 'POST':
        data = request.POST
        if data.get('biscuit', None):
            bisquit = Bisquit.objects.get(id=data['biscuit'])
            text += f'Основа: {bisquit.title}\n'
            characteristics['bisquit'] = bisquit

        if data.get('filling', None):
            filling = Filling.objects.get(id=data['filling'])
            text += f'Начинка: {filling.title} \n'
            characteristics['filling'] = filling

        if formset.is_valid():
            characteristics['decoration'] = []
            characteristics['decoration_price'] = 0
            for form in formset:
                decoration = form.cleaned_data.get('decoration')
                quantity = form.cleaned_data.get('quantity')
                if decoration and quantity:
                    if not decoration_added:
                        text += 'Украшения:\n'
                        decoration_added = True
                    text += f'{decoration.title}: {quantity} штук\n'
                    characteristics['decoration'].append({decoration: quantity})
                    characteristics['decoration_price'] += decoration.price * quantity

        if data.getlist('sprinkles'):
            characteristics['sprinks_price'] = 0
            text += 'Посыпка: '
            sprinks = Sprinkles.objects.filter(id__in=data.getlist('sprinkles'))
            text += ', '.join(sprink.title for sprink in sprinks)
            characteristics['sprinks'] = sprinks
            characteristics['sprinks_price'] += sum(sprink.price for sprink in sprinks)
            text += '\n'

        if data.get('shape'):
            shape = data['shape']
            match shape:
                case 'rectangle':
                    shape_ru = 'прямоугольная'
                case 'circle':
                    shape_ru = 'круг'
            characteristics['shape_ru'] = shape_ru
            text += f'форма уровней {shape_ru} \n'
        if data.get('text_decoration'):
            text_decoration = data.get('text_decoration')
            characteristics['text_decoration'] = text_decoration
            text += f'надпись на торте: {text_decoration}\n'
        if data.get('layers'):
            layers = int(data['layers'])
            match layers:
                case 1:
                    text += 'одноярусный\n'
                case 2:
                    text += 'двухъярусный\n'
                case 3:
                    text += 'трехъярусный\n'
            characteristics['volume'] = 0
            return_text = text
            for i in range(1, layers + 1):
                size = data.get(f"size-{i}").split('x')

                if shape == 'rectangle':
                    return_text += f'ярус {i}  длина {size[0]} см. ширина {size[1]} см. высота {size[2]} см.\n'
                    text += f'ярус {i} площадью {2 * (int(size[0]) + int(size[1])) * int(size[2])}\n'
                if shape == 'circle':
                    return_text += f'ярус {i} диаметр {size[0]} см. высота {size[1]} см.\n'
                    text += f'ярус {i} площадью {3.14 * float(size[0]) * (int(size[1]) + int(size[0]) / 2)}\n'
                characteristics['volume'] += volume_calc(shape, size)
            characteristics['volume'] /= 10 ** 6
            characteristics['weight'] = math.ceil(characteristics['volume'] * (
                    characteristics['bisquit'].weight + 0.3 * characteristics['filling'].weight))

            characteristics['price'] = characteristics['volume'] * (
                    characteristics['bisquit'].weight * characteristics['bisquit'].price + 0.3 *
                    characteristics['filling'].weight * characteristics['filling'].price)
            characteristics['price'] += characteristics.get('sprinks_price', 0) + characteristics.get(
                'decoration_price', 0) + 100 if data.get('text_decoration') else 0
            characteristics['price'] = math.ceil(characteristics['price'])
            return_text += f"масса: {characteristics['weight']} кг.\n"
            return_text += f"цена: {characteristics['price']} руб.\n"
            # push_and_get_photo('Сделай картинку торта: \n'+text)
            cook_time = bisquit.cooking_time + filling.cooking_time
            hour, minutes = convert_minutes_to_hours_and_minutes(cook_time)
            return_text += f'время готовности {hour}ч.:{minutes} мин.'
            orders = Order.objects.filter(state='in_job').values_list('consrt__cook_time', flat=True)
            print(orders)

            context = {'text': return_text, 'image_url': f'/media/fl.jpg?ts={int(time.time())}'}
            return JsonResponse(context)


@login_required(login_url=reverse_lazy('auth'))
def cart_view(request):
    context = {
        'title': 'корзины',
        'user': UserProxy.objects.get(pk=request.user.pk),
        'orders': request.user.orders.all()
    }
    data = request.POST or None
    if data:
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
                          num_order=current_order_num, payment_summ=cart.get_pos_sum()))
            Order.objects.bulk_create(orders)
            Cart.objects.filter(id__in=select_cart).delete()

        if select_consrt_cart:
            orders = []
            for cart_id in select_consrt_cart:
                cart = CartConstructor.objects.get(id=int(cart_id))
                orders.append(
                    Order(user=request.user, consrt=cart.data, quantity=cart.quantity, place=place, payment=pay,
                          num_order=current_order_num, payment_summ=cart.get_sum()))
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
