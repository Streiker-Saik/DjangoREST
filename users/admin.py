from django.contrib import admin

from .models import User


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    """
    Класс для работы администратора с пользователями
    Атрибуты:
        ordering - сортировка по email
        list_filter - фильтрация активный пользователь или нет
        exclude - исключит поле пароля
        list_display - выводит на экран: email, имя, фамилия, супер юзер, сотрудник, активный
        search_fields - поиск по: email
    """

    ordering = ("email",)
    list_filter = ("is_active",)
    exclude = ("password",)
    list_display = (
        "email",
        "first_name",
        "last_name",
        "is_superuser",
        "is_staff",
        "is_active",
    )
    search_fields = ("email",)
