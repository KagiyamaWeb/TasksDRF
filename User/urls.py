from django.urls import path, re_path

from User.views import (RoleListView, RoleCreateView, RoleDeleteView, 
                    RoleUpdateView, UserInfoRetrieveView, 
                    UpdateUserInfo, RoleDetailView)


app_name = 'user'


urlpatterns = (
    path('<int:pk>/', UserInfoRetrieveView.as_view(), name="user_detail"),
    path("update/<int:pk>/", UpdateUserInfo.as_view(), name="user_update"),
    path('roles/', RoleListView.as_view(), name="roles_list"),
    path('roles/<int:pk>/', RoleDetailView.as_view(), name="role_detail"),
    path('roles/delete/<int:pk>/', RoleDeleteView.as_view(), name="role_delete"),
    path('roles/create/', RoleCreateView.as_view(), name="role_create"),
    path('roles/update/<int:pk>/', RoleUpdateView.as_view(), name="role_update"),
)