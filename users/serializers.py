from rest_framework.serializers import ModelSerializer

from users.models import User


class UserSerializer(ModelSerializer):
    """
    Сериализатор для модели Users.
    Показывает поля: id, first_name, last_name, phone_number, city.
    """

    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "phone_number", "city")
