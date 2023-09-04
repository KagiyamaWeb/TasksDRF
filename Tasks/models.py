from django.db import models
from User.models import User


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=1023)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_tasks')