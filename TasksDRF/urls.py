from django.contrib import admin
from django.urls import path, include, re_path


urlpatterns = (
    path('admin/', admin.site.urls),
    path('tasks/', include('Tasks.urls')),
    path('user/', include('User.urls')),
    path('tasks_auth/', include('Auth.urls')),

    re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.jwt')),
)