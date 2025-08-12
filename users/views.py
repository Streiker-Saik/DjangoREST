from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated

from users.models import Payment, User
from users.permissions import IsProfileOwner
from users.serializers import PaymentSerializer, UserCreateSerializer, UserGeneralSerializer, UserSerializer


class UserListAPIView(ListAPIView):
    """
    Представление для получения списка всех пользователей (GET)
    Методы:
        get_serializer_class(self):
            Определяет, какой сериализатор использовать для ответа.
            Возвращает UserSerializer для администраторов, а UserGeneralSerializer для обычных пользователей.
    """

    queryset = User.objects.all()

    def get_serializer_class(self):
        """
        Определяет, какой сериализатор использовать для ответа.
        Возвращает UserSerializer для администраторов, а UserGeneralSerializer для обычных пользователей.
        """
        user = self.request.user
        if user.is_staff:
            return UserSerializer
        return UserGeneralSerializer


class UserCreateAPIView(CreateAPIView):
    """
    Представление для создания пользователя (POST)
    Методы:
        perform_create(self, serializer) -> None:
            Сохраняет нового пользователя и устанавливает его активным.
    """

    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer) -> None:
        """Сохраняет нового пользователя и устанавливает его активным."""
        user = serializer.save(is_active=True)


class UserRetrieveAPIView(RetrieveAPIView):
    """
    Представление для получения пользователя по идентификатору (GET)
    Методы:
        get_serializer_class(self):
            Определяет, какой сериализатор использовать для ответа.
            Возвращает UserSerializer для администраторов и владельца,
            а UserGeneralSerializer для обычных пользователей.
    """

    queryset = User.objects.all()

    def get_serializer_class(self):
        """
        Определяет, какой сериализатор использовать для ответа.
        Возвращает UserSerializer для администраторов и владельца, а UserGeneralSerializer для обычных пользователей.
        """
        user = self.request.user
        pk = self.kwargs.get("pk")
        if pk is None:
            return UserSerializer
        user_profile = get_object_or_404(User, pk=pk)
        if user == user_profile or user.is_staff:
            return UserSerializer
        else:
            return UserGeneralSerializer


class UserUpdateAPIView(UpdateAPIView):
    """Представление для обновления пользователя по идентификатору (PUT/PATH)"""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsProfileOwner]


class UserDestroyAPIView(DestroyAPIView):
    """Представление для удаления пользователя по идентификатору (DELETE)"""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]


class PaymentListAPIView(ListAPIView):
    """
    Представление для получения списка всех платежей (GET)
    Сортировка: дате(date_pay)
    Фильтрация: курсу(course), уроку(lesson), методу платежа(payment_method)
    """

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAdminUser]
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ("date_pay",)
    filterset_fields = (
        "course",
        "lesson",
        "payment_method",
    )
