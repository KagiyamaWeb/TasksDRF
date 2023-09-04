from rest_framework import serializers
from Tasks.models import Task
from User.models import User


class TaskSerializer(serializers.ModelSerializer[Task]):
    class Meta:
        model = Task
        fields = '__all__'


class TaskCreateSerializer(serializers.ModelSerializer[Task]):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    assigned_to = serializers.SlugRelatedField(slug_field="pk", queryset=User.objects.all())

    class Meta:
        model = Task
        fields = (
            'created_by',
            'assigned_to',
            'description',
            'title'
        )


class TaskUpdateSerializer(serializers.ModelSerializer[Task]):
    assigned_to = serializers.SlugRelatedField(slug_field="pk", queryset=User.objects.all())

    class Meta:
        model = Task
        fields = (
            'assigned_to',
            'description',
            'title'
        )