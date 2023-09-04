import factory
from factory.django import DjangoModelFactory
from django.db.models.signals import post_save

from User.factory import UserFactory
from Tasks.models import Task


@factory.django.mute_signals(post_save)
class TaskFactory(DjangoModelFactory):
    class Meta:
        model = Task

    assigned_to = factory.SubFactory(UserFactory)
    created_by = factory.SubFactory(UserFactory)

    title = factory.Faker("text", max_nb_chars=255)
    description = factory.Faker("text", max_nb_chars=1023)