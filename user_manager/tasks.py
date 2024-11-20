import smtplib
from diplom.celery import app
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# Укажите ваши учетные данные
username = 'erbolbaik@mail.ru'  # Ваш email
password = 'kqhr0eEnyDBuARiUnGVN'         # Ваш пароль
smtp_server = 'smtp.mail.ru'
smtp_port = 587
# Настройка параметров письма
sender_email = username


@app.task
def send_verification_email(subj:str, mess:str, to_email:str):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = 'регистрация Карамелька'
    # Добавление текста в сообщение
    body=mess
    msg.attach(MIMEText(body, 'plain'))
    try:
    # Подключение к SMTP-серверу и отправка сообщения
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Защищенное соединение
        server.login(username, password)  # Вход в учетную запись
        server.send_message(msg)  # Отправка сообщения
        print('Сообщение успешно отправлено!')
    except Exception as e:
        print(f'Произошла ошибка: {e}')
    finally:
        server.quit()  # Закрытие соединения