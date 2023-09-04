from rest_framework import status, permissions, generics
from rest_framework.response import Response
from django.contrib.auth.models import Group

from User.permissions import IsAdmin
from drf_yasg.utils import swagger_auto_schema
from User.serializers import (UserSerializer, RoleSerializer, 
                              UserUpdateSerializer, AdminUserUpdateSerializer)
from User.models import Role, User


def is_admin_role(user):
    if user.roles.filter(id=2).exists():
        return True
    return False


class UserInfoRetrieveView(generics.RetrieveAPIView):
    """
    API class to Info about user by id
    """
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = UserSerializer
    lookup_field = "pk"

    @swagger_auto_schema(
        responses={
            404: "Пользователь не найден, или не-админ запросил информацию не о себе",
            401: "Пользователь не авторизован",
        }
    )
    def get(self, request, *args, **kwargs):
        user = request.user
        if not user or (not is_admin_role(user) and user.id != kwargs['pk']):
            return Response(
                {"detail": "Пользователь не найден, или не-админ запросил информацию не о себе"},
                 status=status.HTTP_404_NOT_FOUND
                 )
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        if user.roles.filter(id=2).exists():
            return User.objects.all()
        else:
            return User.objects.filter(pk=user.id)


class UpdateUserInfo(generics.UpdateAPIView):
    http_method_names = ["patch"]
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserUpdateSerializer

    def get_queryset(self):
        user = self.request.user
        if is_admin_role(user):
            return User.objects.all()
        else:
            return User.objects.filter(pk=user.id)
    
    def get_serializer_class(self):
        user = self.request.user
        if is_admin_role(user):
            return AdminUserUpdateSerializer
        else:
            return UserUpdateSerializer
    
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        
        user = self.request.user
        if 'roles' in request.data and not is_admin_role(user):
            return Response(
                {'detail': 'Пользователь не может менять свои роли.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class RoleDetailView(generics.RetrieveAPIView):
    serializer_class = RoleSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.set_view(request.user)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get_queryset(self):
        user = self.request.user
        if is_admin_role(user):
            return Role.objects.all()
        else:
            return user.roles.all()


class RoleListView(generics.ListAPIView):
    """
    API class shows a list of user Roles
    Raise http 401 error if user is Anonymous
    """
    serializer_class = RoleSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        user = self.request.user
        if is_admin_role(user):
            return Role.objects.all()
        else:
            return user.roles.all()


class RoleCreateView(generics.CreateAPIView):
    permission_classes = (IsAdmin, )
    serializer_class = RoleSerializer


class RoleUpdateView(generics.UpdateAPIView):
    permission_classes = (IsAdmin, )
    serializer_class = RoleSerializer
    queryset = Role.objects.all()


class RoleDeleteView(generics.DestroyAPIView):
    permission_classes = (IsAdmin, )
    queryset = Role.objects.all()