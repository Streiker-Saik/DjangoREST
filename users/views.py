from django.shortcuts import render
from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework.viewsets import ModelViewSet

from users.models import User
from users.serializers import UserSerializer


class UserViewSet(ModelViewSet):
    """
    Представление набора действий для модели Course.
    Позволяет выполнять операции с курсами:
        отображение списка, создание, отображение, полное обновление, частичное обновление, удаление.
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()
