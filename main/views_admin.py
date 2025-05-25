import json
import smtplib
import threading
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from webpush import send_user_notification

from .models import Order, Comment

# Укажите ваши учетные данные
username = 'erbolbaik@mail.ru'  # Ваш email
password = 'kqhr0eEnyDBuARiUnGVN'  # Ваш пароль

# Настройка параметров письма
sender_email = username

# Создание MIME-объекта
msg = MIMEMultipart()
msg['From'] = sender_email


def send_email(email_to: str, text: str, subject: str):
    try:
        # Создаем SSL-соединение
        with smtplib.SMTP_SSL("smtp.mail.ru", 465) as server:
            body = text
            msg['Subject'] = subject
            # Добавление текста в письмо
            msg.attach(MIMEText(body, 'plain'))
            server.login(username, password)  # Вход в почтовый ящик
            server.sendmail(sender_email, email_to,
                            msg.as_string())  # Отправка письма
    except smtplib.SMTPException as e:
        print(f"Ошибка при подключении или аутентификации: {e}")


def send_notify(user, body_text):
    if user is not None:
        payload = {"head": "Привет!", "body": body_text}
        send_user_notification(user=user, payload=payload, ttl=1000)


@staff_member_required
def order_ready(request, pk: int):
    order = Order.objects.get(id=pk)
    order.state = 'ready'
    order.save()
    # Отправляем уведомление
    notify_thread = threading.Thread(target=send_notify(order.user, f'{order} готов'))
    email_thread = threading.Thread(target=send_email(order.user.email, f'заказ {order.id} готов', 'карамелька'))
    notify_thread.start()
    email_thread.start()
    # Запускаем асинхронную функцию в синхронном контексте
    return redirect(request.META.get('HTTP_REFERER'))


@staff_member_required
def order_processing(request):
    orders = Order.objects.filter(status=False).order_by('-created_at', 'user')
    context = {
        'title': 'обработка заказов',
        'object_list': orders,
    }
    return render(request, 'main/templates/for_admin/order_processing.html', context=context)


@staff_member_required
def order_status(request, pk: int):
    order = Order.objects.get(id=pk)
    order.status = True
    order.status_at = datetime.now()
    order.save()
    return redirect(request.META.get('HTTP_REFERER'))


@staff_member_required
def moderate_comments(request):
    comments = Comment.objects.filter(moderated=False)
    context = {
        'title': 'обработка заказов',
        'comments': comments,
    }
    return render(request, 'main/templates/for_admin/moderate_comments.html', context=context)


@staff_member_required
def app_del_comments(request, fun: str, pk: int):
    comment = Comment.objects.get(id=pk)
    match fun:
        case 'del':
            comment.delete()
        case 'apply':
            comment.apply()

    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url=reverse_lazy('auth'))
def configs(request):
    def convert_to_float(value):
        return float(value.replace(',', '.'))
    context = {}
    with open('main/LayerSize.json') as lf:
        layers = json.load(lf)
        context['layers'] = layers
    with open('main/coefficient.json') as cf:
        coef = json.load(cf)
        context['coef'] = coef
    if request.method == 'POST':
        data = request.POST
        data_dict = {
            "decoration": convert_to_float(data.get('decoration', 0)),
            "sprinkles": convert_to_float(data.get('sprinkles', 0)),
            "shape": {
                "rectangle": convert_to_float(data.get('rectangle', 0)),
                "circle": convert_to_float(data.get('circle', 0))
            },
            "layers": convert_to_float(data.get('layers', 0))
        }
        with open('main/coefficient.json','w') as json_file:
            json.dump(data_dict, json_file, indent=4)
            return redirect('configs')
    return render(request, 'main/templates/for_admin/configs.html', context=context)
