from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated

from users.models import Payment, User, TransactionStripe
from users.permissions import IsProfileOwner
from users.serializers import PaymentSerializer, UserCreateSerializer, UserGeneralSerializer, UserSerializer, \
    TransactionStripeSerializer
from users.services import TransactionStripeService


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

    @swagger_auto_schema(
        operation_description="Полное обновление пользователя",
        operation_id="users_update"
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Частичное обновление пользователя",
        operation_id="users_partial_update"
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


class UserDestroyAPIView(DestroyAPIView):
    """Представление для удаления пользователя по идентификатору (DELETE)"""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(operation_id="users_delete")
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class PaymentListAPIView(ListAPIView):
    """
    Представление для получения списка всех платежей (GET)
    Сортировка: дате(date_pay)
    Фильтрация: курсу(course), уроку(lesson), методу платежа(payment_method)
    """

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    # permission_classes = [IsAdminUser]
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ("date_pay",)
    filterset_fields = (
        "course",
        "lesson",
        "payment_method",
    )


class PaymentCreateAPIView(CreateAPIView):
    """
    Представление для создания платежа (POST)
    Методы:
        perform_create(self, serializer) -> None:
            Сохраняет платеж и обрабатывает создание сессии Stripe.
    """

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def perform_create(self, serializer) -> None:
        """Сохраняет платеж и обрабатывает создание сессии Stripe."""
        payment = serializer.save(user=self.request.user)

        if payment.payment_method == "transfer":
            course_name = payment.course.title
            amount = payment.amount
            product = TransactionStripeService.get_strip_product(product_name=course_name)
            price = TransactionStripeService.get_strip_price(amount=amount, product_id=product.get("id"))
            strip_pay_id, url_link = TransactionStripeService.create_strip_session(price)

            transaction_data = {"payment": payment.id, "strip_pay_id": strip_pay_id,"url_link": url_link}
            transaction = TransactionStripeSerializer(data=transaction_data)
            transaction.is_valid(raise_exception=True)
            transaction.save()

