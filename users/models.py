from django.contrib.auth.models import AbstractUser
from django.db import models

from lms.models import Course, Lesson


class User(AbstractUser):
    """
    Представление кастомного пользователя, расширяющее AbstractUser.
    Поле авторизации с username изменено на email.
    Так же username обязательное поле при авторизации
    Атрибуты:
        username: Логин отключен
        email(str): Уникальный email
        phone_number(str): Номер телефона
        city(str): Город
        avatar(ImageField): Аватар (изображение)
    """

    username = None
    email = models.EmailField(unique=True, verbose_name="Email")
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name="Номер телефона")
    city = models.CharField(max_length=65, blank=True, null=True, verbose_name="Город")
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True, verbose_name="Аватар")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self) -> str:
        """
        Строковое представление класса.
        :return: Email
        """
        return f"{self.email}"

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"


class Payment(models.Model):
    """
    Представление платежа
    Атрибуты:
        user(ForeignKey): Пользователь (внешний ключ на модель «Пользователя»)
        date_pay(datetime): Дата платежа
        course(ForeignKey): Курс (внешний ключ на модель «Курс»)
        lesson(ForeignKey): Урок (внешний ключ на модель «Урок»)
        amount(int): Сумма платежа
        payment_method(str): Способ оплаты. Возможные значения:
            cash - Наличные,
            transfer - Перевод на счет
    """

    PAYMENT_METHOD_CHOICES = [
        ("cash", "Наличные"),
        ("transfer", "Перевод на счет"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments", verbose_name="Пользователь")
    date_pay = models.DateField(verbose_name="Дата оплаты")
    course = models.ForeignKey(
        Course, on_delete=models.SET_NULL, related_name="payments", blank=True, null=True, verbose_name="Курс"
    )
    lesson = models.ForeignKey(
        Lesson, on_delete=models.SET_NULL, related_name="payments", blank=True, null=True, verbose_name="Урок"
    )
    amount = models.PositiveIntegerField(verbose_name="Сумма оплаты")
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES, verbose_name="Способ оплаты")

    def __str__(self) -> str:
        """
        Строковое представление платежа
        :return: Оплачено: Дата - ..., Сумма - ...
        """
        return f"Оплачено: Дата - {self.date_pay}, Сумма - {self.amount}"

    class Meta:
        verbose_name = "платеж"
        verbose_name_plural = "платежи"
