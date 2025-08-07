from django.db import models

from config import settings


class Course(models.Model):
    """
    Представление курса
    Атрибуты:
        title(str): Название курса
        preview(ImageField): Превью курса
        description(str): Описание курса
        owner(ForeignKey): Владелец (внешний ключ на модель User(Пользователь))
    """

    title = models.CharField(max_length=255, verbose_name="Название курса")
    preview = models.ImageField(upload_to="courses/previews/", blank=True, null=True, verbose_name="Превью курса")
    description = models.TextField(blank=True, null=True, verbose_name="Описание курса")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="courses",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Владелец",
    )

    def __str__(self) -> str:
        """
        Строковое представление курса
        :return: Название курса
        """
        return f"{self.title}"

    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "курсы"


class Lesson(models.Model):
    """
    Представление урока
    Атрибуты:
        title(str): Название урока
        description(str): Описание урока
        preview(ImageField): Превью урока
        video_url(URLField): Ссылка на видео
        courses(ForeignKey): Курс (внешний ключ на модель Course(Курс))
        owner(ForeignKey): Владелец (внешний ключ на модель User(Пользователь))
    """

    title = models.CharField(max_length=255, verbose_name="Название урок")
    description = models.TextField(blank=True, null=True, verbose_name="Описание урока")
    preview = models.ImageField(upload_to="courses/previews/", blank=True, null=True, verbose_name="Превью урока")
    video_url = models.URLField(blank=True, null=True, verbose_name="Ссылка на видео")
    courses = models.ForeignKey(Course, related_name="lessons", on_delete=models.CASCADE, verbose_name="Курс")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="lessons",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Владелец",
    )

    def __str__(self) -> str:
        """
        Строковое представление урока
        :return: Название урока
        """
        return f"{self.title}"

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки"


class Subscription(models.Model):
    """
    Представление подписки
    Атрибуты:
        user(ForeignKey): Пользователь (внешний ключ на модель User(Пользователь))
        course(ForeignKey): Курс (внешний ключ на модель Course(Курс))
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="subscriptions",
        on_delete=models.CASCADE,
        verbose_name="Пользователь"
    )
    course = models.ForeignKey(Course, related_name="subscriptions", on_delete=models.CASCADE, verbose_name="Курс")

    def __str__(self) -> str:
        """
        Строковое представление подписки
        :return: пользователь: ... - курс ...
        """
        return f"пользователь: {self.user} - курс {self.course}"

    class Meta:
        verbose_name = "подписка"
        verbose_name_plural = "подписки"
