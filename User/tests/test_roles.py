import pytest

from User.models import Role, User

from django.urls import reverse
from rest_framework import status as http_status


from User.models import Role


class TestRoleCreateView():
    versions = ("v1",)
    url = "user:role_create"

    @pytest.mark.django_db
    @pytest.mark.parametrize("payload", ({
                                            "description": "test",
                                            "name": "test_role",
                                         }, {
                                            "description": "test",
                                            "name": "test_tole2"
                                         },))
    def test_view(self, auth_admin, payload):
        url = reverse(self.url)

        response = auth_admin.post(url, payload)
        assert response.status_code == http_status.HTTP_201_CREATED

    @pytest.mark.django_db
    def test_view_by_anonymous(self, client):
        url = reverse(self.url)
        res = client.post(url)
        assert res.status_code == http_status.HTTP_401_UNAUTHORIZED

    @pytest.mark.django_db
    def test_view_by_base_user(self, auth_user):
        url = reverse(self.url)
        res = auth_user.post(url)
        assert res.status_code == http_status.HTTP_403_FORBIDDEN


class TestListRoleView():
    url = "user:roles_list"

    @pytest.mark.django_db
    def test_view_by_user(self, auth_user):
        url = reverse(self.url)

        response = auth_user.get(url)
        response_json = response.json()

        role_count = len(User.objects.get(pk=1).roles.all())

        assert len(response_json) == role_count

    @pytest.mark.django_db
    def test_view_by_admin(self, auth_admin):
        url = reverse(self.url)
        response = auth_admin.get(url)
        response_json = response.json()

        role_count = Role.objects.all().count()

        assert len(response_json) == role_count

    @pytest.mark.django_db
    def test_view_by_anonymous(self, client):
        url = reverse(self.url)
        res = client.get(url)

        assert res.status_code == http_status.HTTP_401_UNAUTHORIZED


class TestRoleUpdateView():
    versions = ("v1",)
    url = "user:role_update"

    @pytest.mark.django_db
    def test_view_by_anonymous(self, client):
        url = reverse(self.url, kwargs={
            "pk": 2
        })

        res = client.patch(url)
        assert res.status_code == http_status.HTTP_401_UNAUTHORIZED

    @pytest.mark.django_db
    @pytest.mark.parametrize("payload", [{
        "description": "another_discription"
    }])
    def test_update_by_another_user(self, auth_user, payload):
        url = reverse(self.url, kwargs={
            "pk": 2
        })

        res = auth_user.patch(url)
        assert res.status_code == http_status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_update_role_by_another_user(self, auth_user):
        for pk in [1, 2]:
            url = reverse(self.url, kwargs={
                "pk": pk
            })
            res = auth_user.patch(url)

            assert res.status_code == http_status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_update_role_by_admin(self, auth_admin):
        for pk in [1, 2]:
            url = reverse(self.url, kwargs={
                "pk": pk
            })
            res = auth_admin.patch(url, data={'description': 'test_description'}, content_type='application/json')

            assert res.status_code == http_status.HTTP_200_OK

