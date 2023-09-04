import factory
from factory.django import DjangoModelFactory
from django.db.models.signals import post_save

from User.models import User


@factory.django.mute_signals(post_save)
class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.LazyAttribute(lambda o: f"user_{o.email}")
    email = factory.Faker("email")    