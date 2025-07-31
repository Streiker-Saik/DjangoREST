from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView

from users.models import User, Payment
from users.serializers import UserSerializer, PaymentSerializer


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

class PaymentListAPIView(ListAPIView):
    """
    Представление для получения списка всех платежей (GET)
    Сортировка: дате(date_pay)
    Фильтрация: курсу(course), уроку(lesson), методу платежа(payment_method)
    """

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ["date_pay"]
    filterset_fields = ["course", "lesson", "payment_method"]
