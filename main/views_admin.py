from .models import Order
from django.shortcuts import render, redirect
from datetime import datetime

def order_processing(request):
    orders = Order.objects.filter(status=False).order_by('-created_at','user')
    context = {
        'title': 'обработка заказов',
        'object_list': orders,
    }
    return render(request, 'main/templates/for_admin/order_processing.html', context=context)

def order_ready(request,pk:int):
    order = Order.objects.get(id=pk)
    order.state = 'ready'
    order.save()
    return redirect(request.META.get('HTTP_REFERER'))

def order_status(request,pk:int):
    order = Order.objects.get(id=pk)
    order.status = True
    order.status_at = datetime.now()
    order.save()
    return redirect(request.META.get('HTTP_REFERER'))