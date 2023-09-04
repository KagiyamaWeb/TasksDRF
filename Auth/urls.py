from django.urls import path
#from rest_framework_simplejwt.views import TokenRefreshView

from Auth.views import CustomObtainTokenPairView


app_name = "auth"

urlpatterns = (
    #path("jwt/create/", CustomObtainTokenPairView.as_view(), name="jwt-create"),
    #path('jwt/refresh/') для обновления токена
)