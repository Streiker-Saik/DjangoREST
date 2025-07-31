from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from users.models import Payment, User


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
    """

    class Meta:
        model = Payment
        fields = "__all__"


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
