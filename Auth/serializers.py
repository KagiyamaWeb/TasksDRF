import re

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from django.db import IntegrityError


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["roles"] = list(user.roles.values_list("name", flat=True))
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        return data


def validate_email(email):
    if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
        raise serializers.ValidationError({"email": "Неверный адрес электронной почты"})

class UserRegistrationSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        #model = User
        fields = UserCreateSerializer.Meta.fields

    def validate(self, attrs):
        validate_email(attrs["email"])
        return super().validate(attrs)

    def create(self, validated_data):
        try:
            user = self.perform_create(validated_data)
        except IntegrityError:
            self.fail("cannot_create_user")
        return user