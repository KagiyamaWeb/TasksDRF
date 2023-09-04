from django.urls import path
from Tasks.views import (CreateTaskView, UpdateTaskView, 
                         GetTaskView, DeleteTaskView, ListTaskView)


app_name = 'tasks'


urlpatterns = (
    path('create/', CreateTaskView.as_view(), name="task_create"),
    path('update/<int:pk>/', UpdateTaskView.as_view(), name="task_update"),
    path('get/<int:pk>/', GetTaskView.as_view(), name="task_detail"),
    path('delete/<int:pk>', DeleteTaskView.as_view(), name="task_delete"),
    path('list/', ListTaskView.as_view(), name="tasks_list"),
)