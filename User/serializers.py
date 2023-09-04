import re

from rest_framework import serializers
from django.db import IntegrityError
from User.models import Role, User
from djoser.serializers import UserCreateSerializer
from rest_framework_simplejwt.tokens import RefreshToken


def validate_email(email):
    if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
        raise serializers.ValidationError({"email": "Неверный адрес электронной почты"})


class RoleSerializer(serializers.ModelSerializer[Role]):

    class Meta:
        model = Role
        fields = '__all__'


class CustomUserCreateSerializer(UserCreateSerializer):
    roles = RoleSerializer(many=True, required=False, allow_null=True)

    class Meta:
        fields = ('username', 'email', 'roles')

    def validate(self, attrs):
        validate_email(attrs["username"])
        if "username" in attrs and "email" not in attrs:
            attrs["email"] = attrs["username"]
        return super().validate(attrs)

    def create(self, validated_data):
        try:
            user = self.perform_create(validated_data)
        except IntegrityError:
            self.fail("cannot_create_user")
        return user


class UserSerializer(serializers.ModelSerializer[User]):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'roles')


class UserUpdateSerializer(serializers.ModelSerializer[User]):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'roles'
        )

class AdminUserUpdateSerializer(UserUpdateSerializer):
    roles = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), required=False, many=True)