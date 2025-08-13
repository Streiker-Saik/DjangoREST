from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from users.models import Payment, User, TransactionStripe


class TransactionStripeSerializer(ModelSerializer):
    """
    Сериализатор для модели TransactionStripe.
    Показывает поля:
        id(int): Уникальный идентификатор транзакции
        payment(ForeignKey): Внешний ключ на платеж.
        strip_pay_id(str): Идентификатор транзакции.
        url_link(str): Ссылка на оплату.
    """

    class Meta:
        model = TransactionStripe
        fields = "__all__"


class PaymentSerializer(ModelSerializer):
    """
    Сериализатор для модели Payment.
    Показывает поля:
        id(int): Уникальный идентификатор платежа.
        date_pay(datetime): Дата платежа.
        amount(str): Сумма платежа.
        payment_method(str): Метод платежа.
        user(ForeignKey): Внешний ключ на пользователя.
        course(ForeignKey): Внешний ключ на курс.
        lesson(ForeignKey): Внешний ключ на урок.
        transaction_info(list): Список транзакций
    """
    transaction_info = TransactionStripeSerializer(many=True, read_only=True, source='transactions')

    class Meta:
        model = Payment
        fields = ('course', 'lesson', 'amount', 'payment_method', 'transaction_info')


class UserSerializer(ModelSerializer):
    """
    Сериализатор для модели Users.
    Показывает поля:
        id(int): Уникальный идентификатор пользователя.
        first_name(str): Имя пользователя.
        last_name(str): Фамилия пользователя.
        phone_number(str): Номер телефона пользователя.
        city(str): Город пользователя.
        history_pay(list): Список платежей(PaymentSerializer)
        payments(list): Список платежей (PaymentSerializer)
    """

    payments = PaymentSerializer(many=True)

    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "phone_number", "city", "payments")


class UserGeneralSerializer(ModelSerializer):
    """
    Сериализатор общей информации для модели Users.
    Показывает поля:
        id(int): Уникальный идентификатор пользователя
        email(str): Почта пользователя
        city(str): Город пользователя.
    """

    class Meta:
        model = User
        fields = ("id", "email", "city")


class UserCreateSerializer(ModelSerializer):
    """
    Сериализатор для создания модели Users.
    Показывает поля:
        id(int): Уникальный идентификатор пользователя
        email(str): Почта пользователя
        phone_number(str): Номер телефона пользователя
        city(str): Город пользователя.
    """

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("id", "email", "phone_number", "city", "password")

    def create(self, validated_data):
        """Создает нового пользователя и хэширует его пароль."""
        user = User(**validated_data)
        user.set_password(validated_data.pop("password"))
        user.save()
        return user
