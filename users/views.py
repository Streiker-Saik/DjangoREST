from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView

from users.models import User
from users.serializers import UserSerializer


class UserListAPIView(ListAPIView):
    """Представление для получения списка всех пользователей (GET)"""

    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserRetrieveAPIView(RetrieveAPIView):
    """Представление для получения пользователя по идентификатору (GET)"""

    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserUpdateAPIView(UpdateAPIView):
    """Представление для обновления пользователя по идентификатору (PUT/PATH)"""

    serializer_class = UserSerializer
    queryset = User.objects.all()
