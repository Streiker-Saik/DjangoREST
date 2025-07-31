from rest_framework.serializers import ModelSerializer

from users.models import User


class UserSerializer(ModelSerializer):
    """
    Сериализатор для модели Users.
    Показывает поля:
        id(int): Уникальный идентификатор пользователя.
        first_name(str): Имя пользователя.
        last_name(str): Фамилия пользователя
        phone_number(str): Номер телефона пользователя.
        city(str): Город пользователя.
    """

    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "phone_number", "city")
