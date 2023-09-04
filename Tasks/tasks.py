from celery import shared_task
from django.core.mail import EmailMessage


@shared_task
def send_task_notification_email(email, subject, message):
    email = EmailMessage(subject, message, to=[email])
    email.send()