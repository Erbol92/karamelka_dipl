from django.core.mail import EmailMessage 
from diplom.celery import app

@app.task
def send_verification_email(subj:str, mess:str, to_email:str):
    email = EmailMessage( 
                    subj, mess, to=[to_email] 
        )
    email.content_subtype = "html"
    email.send()
    print('sended')