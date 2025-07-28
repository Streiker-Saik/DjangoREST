from rest_framework.serializers import ModelSerializer

from users.models import User


class UserSerializer(ModelSerializer):
    """Сериализатор для модели Users"""

    class Meta:
        model = User
        exclude = ("password",)
