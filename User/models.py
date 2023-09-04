from django.db import models
from django.contrib.auth.models import Group
from django.contrib.auth.models import AbstractUser


class Role(Group):
    description = models.TextField(max_length=1024)


class User(AbstractUser):
    roles = models.ManyToManyField(
        to=Role,
        through="UserRole",
        related_name="users",
        null=True,
    )


class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    class Meta:
        db_table = "user_roles"
