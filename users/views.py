from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny

from users.models import Payment, User
from users.serializers import PaymentSerializer, UserCreateSerializer, UserSerializer


class UserListAPIView(ListAPIView):
    """Представление для получения списка всех пользователей (GET)"""

    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserCrateAPIView(CreateAPIView):
    """Представление для создания пользователя (POST)"""

    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        """Сохраняет нового пользователя и устанавливает его активным."""
        user = serializer.save(is_active=True)


class UserRetrieveAPIView(RetrieveAPIView):
    """Представление для получения пользователя по идентификатору (GET)"""

    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserUpdateAPIView(UpdateAPIView):
    """Представление для обновления пользователя по идентификатору (PUT/PATH)"""

    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserDestroyAPIView(DestroyAPIView):
    """Представление для удаления пользователя по идентификатору (DELETE)"""

    serializer_class = UserSerializer
    queryset = User.objects.all()


class PaymentListAPIView(ListAPIView):
    """
    Представление для получения списка всех платежей (GET)
    Сортировка: дате(date_pay)
    Фильтрация: курсу(course), уроку(lesson), методу платежа(payment_method)
    """

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ("date_pay",)
    filterset_fields = (
        "course",
        "lesson",
        "payment_method",
    )
