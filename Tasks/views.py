from rest_framework import permissions, generics
from rest_framework.response import Response

from Tasks.models import Task
from Tasks.serializers import TaskSerializer, TaskCreateSerializer, TaskUpdateSerializer
from User.permissions import IsAdmin
from User.models import User


class GetTaskView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.set_view(request.user)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)



class ListTaskView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = TaskSerializer

    def get_queryset(self):
        user = self.request.user
        if user.roles.filter(id=2).exists():
            return Task.objects.all()
        else:
            return Task.objects.filter(assigned_to=user)


class UpdateTaskView(generics.UpdateAPIView):
    permission_classes = (IsAdmin, )
    serializer_class = TaskUpdateSerializer
    queryset = Task.objects.all()

    '''
    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.set_share(request.user)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    '''

class CreateTaskView(generics.CreateAPIView):
    """
    API class to CREATE Task by pk
    Raise http 403 error if user is not admin
    Raise http 401 error if user is Anonymous
    """
    permission_classes = (IsAdmin,)
    serializer_class = TaskCreateSerializer


class DeleteTaskView(generics.DestroyAPIView):
    """
    API class to DELETE Task by pk
    Raise http 403 error if user is not admin
    Raise http 401 error if user is Anonymous
    Raise http 404 error if no Task with requested pk
    """
    queryset = Task.objects.all()
    permission_classes = (IsAdmin, )