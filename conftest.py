import pytest
from pytest_factoryboy import register

from django.conf import settings
from django.core.management import call_command
from django.contrib.auth.models import Group, AnonymousUser
from django.test.client import Client
import TasksDRF.settings as settings

from rest_framework_simplejwt.tokens import RefreshToken

from User.factory import UserFactory
from Tasks.factory import TaskFactory
from User.models import User


DJANGO_SETTINGS_MODULE = settings

register(UserFactory)
register(TaskFactory)



@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    fixtures_to_load = (
        "roles",
        "users",
    )
    with django_db_blocker.unblock():
        for i in fixtures_to_load:
            call_command("loaddata", i)


def authenticate_user(user: User) -> Client:
    client = Client()
    refresh = RefreshToken.for_user(user)
    client.defaults["HTTP_AUTHORIZATION"] = f"Bearer {refresh.access_token}"
    return client

@pytest.fixture
@pytest.mark.django_db
def user():
    user = User.objects.get(pk=1)

    yield user


@pytest.fixture
def anonymous_user():
    return AnonymousUser()


@pytest.fixture
def admin():
    admin = User.objects.get(pk=2)

    yield admin


@pytest.fixture
def auth_user(user: User) -> Client:
    return authenticate_user(user)


@pytest.fixture
def auth_admin(admin: User) -> Client:
    return authenticate_user(admin)