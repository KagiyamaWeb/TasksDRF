
from django.db.models.signals import post_save
from django.dispatch import receiver
from Tasks.models import Task
from Tasks.tasks import send_task_notification_email


@receiver(post_save, sender=Task)
def task_created(sender, instance, created, **kwargs):
    if created:
        send_task_notification_email.delay(instance.assigned_to.email, "Task Created", "You have a new task.")


@receiver(post_save, sender=Task)
def task_updated(sender, instance, **kwargs):
    if instance.previous_assigned_to != instance.assigned_to:
        send_task_notification_email.delay(instance.assigned_to.email, "Task Updated", "You have been assigned a task.")