from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import permissions
from Auth.serializers import CustomTokenObtainPairSerializer


class CustomObtainTokenPairView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = CustomTokenObtainPairSerializer