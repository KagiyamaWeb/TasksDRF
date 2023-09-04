import pytest

from faker import Faker
from django.test.client import MULTIPART_CONTENT, encode_multipart, BOUNDARY
from rest_framework import status as http_status
from rest_framework import status
from django.urls import reverse
#from utils.versioning import VersioningTest

from User.models import User
from User.serializers import UserSerializer, UserUpdateSerializer
from User.views import is_admin_role


fake = Faker()


@pytest.mark.django_db
def test_create_user(client):
    user_create_data = {"username": "test_user", "email": fake.email(), "password": fake.password()}
    res = client.post("/auth/users/", user_create_data)

    assert res.status_code == status.HTTP_201_CREATED
    assert res.data["username"] == user_create_data["username"]
    assert res.data["email"] == user_create_data["email"]


class TestUserDetailView():
    url = "user:user_detail"

    @pytest.mark.django_db
    def test_get_user_info_by_another_user(self, auth_user):
        url = reverse(self.url, kwargs={
            "pk": 2
        })
        res = auth_user.get(url)
        
        assert res.status_code == http_status.HTTP_404_NOT_FOUND
    
    @pytest.mark.django_db
    def test_get_user_info_by_user(self, auth_user):
        url = reverse(self.url, kwargs={
            "pk": 1
        })
        res = auth_user.get(url)
        
        assert res.status_code == http_status.HTTP_200_OK

    @pytest.mark.django_db
    def test_get_user_info_by_anonymous(self, client):
        url = reverse(self.url, kwargs={
            "pk": 2
        })
        res = client.get(url)
        assert res.status_code == http_status.HTTP_401_UNAUTHORIZED


class TestUserUpdateView():
    url = "user:user_update"

    @pytest.mark.django_db
    def test_view_by_anonymous(self, client):
        url = reverse(self.url, kwargs={
            "pk": 2
        })

        res = client.patch(url)
        assert res.status_code == http_status.HTTP_401_UNAUTHORIZED

    @pytest.mark.django_db
    def test_update_user_roles_by_user(self, auth_user):
        url = reverse(self.url, kwargs={
            "pk": 1
        })
        roles = {"roles": (1, 2)}
        res = auth_user.patch(url, data=roles, content_type='application/json')

        assert res.status_code == http_status.HTTP_401_UNAUTHORIZED
    
    @pytest.mark.django_db
    def test_update_user_info_by_user(self, auth_user):
        url = reverse(self.url, kwargs={
            "pk": 1
        })
        roles = {"username": "test_username"}
        res = auth_user.patch(url, data=roles, content_type='application/json')

        assert res.status_code == http_status.HTTP_200_OK
    

    @pytest.mark.django_db
    def test_update_user_roles_by_admin(self, auth_admin, user):
        url = reverse(self.url, kwargs={
            "pk": 2
        })
        roles = {"roles": (1, 2)}
        res = auth_admin.patch(url, data=roles, content_type='application/json')

        assert res.status_code == http_status.HTTP_200_OK