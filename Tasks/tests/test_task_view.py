import pytest

from Tasks.models import Task
from User.models import User

from django.urls import reverse
from django.db.models.signals import post_save
from django.core.management import call_command
from rest_framework import status as http_status


@pytest.fixture(scope='class')
def disable_signals():
    """Fixture to temporarily disable signal handlers."""
    post_save.receivers = []
    yield
    post_save.receivers = []

class TestDisableSignals():
    @pytest.fixture(autouse=True)
    def setup_class(self, disable_signals):
        call_command('loaddata', '../fixtures/tasks.yaml')



class TestTaskCreateView(TestDisableSignals):
    url = "tasks:task_create"

    @pytest.mark.django_db
    @pytest.mark.parametrize("payload", ({
                                             "title": "sample_task",
                                             "description": "sample_description",
                                             "assigned_to": 1,
                                         }, {
                                             "title": "sample_task",
                                             "description": "sample_description",
                                             "assigned_to": 2,
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


class TestTaskListView(TestDisableSignals):
    url = "tasks:tasks_list"

    @pytest.mark.django_db
    def test_view(self, auth_user):
        url = reverse(self.url)
        response = auth_user.get(url)
        response_json = response.json()
        user = User.objects.get(pk=1)

        task_count = Task.objects.filter(assigned_to=user).count()

        assert len(response_json) == task_count

    @pytest.mark.django_db
    def test_view_by_anonymous(self, client):
        url = reverse(self.url)
        res = client.get(url)

        assert res.status_code == http_status.HTTP_401_UNAUTHORIZED


class TestTaskUpdateView(TestDisableSignals):
    url = "tasks:task_update"

    @pytest.mark.django_db
    def test_view_by_anonymous(self, client):
        url = reverse(self.url, kwargs={
            "pk": 2
        })

        res = client.patch(url)
        assert res.status_code == http_status.HTTP_401_UNAUTHORIZED

    @pytest.mark.django_db
    def test_update_task_by_admin(self, auth_admin):
        url = reverse(self.url, kwargs={
            "pk": 1
        })

        res = auth_admin.patch(url, data={"assigned_to": 3}, content_type='application/json')

        assert res.status_code == http_status.HTTP_200_OK

    @pytest.mark.django_db
    def test_update_task_by_another_user(self, auth_user):
        url = reverse(self.url, kwargs={
            "pk": 1
        })
        res = auth_user.patch(url, data={"assigned_to": 3}, content_type='application/json')

        assert res.status_code == http_status.HTTP_403_FORBIDDEN


    @pytest.mark.django_db
    def test_update_task_by_anonymous(self, client):
        url = reverse(self.url, kwargs={
            "pk": 2
        })
        res = client.patch(url)
        assert res.status_code == http_status.HTTP_401_UNAUTHORIZED