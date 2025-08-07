from rest_framework import serializers

from lms.models import Course, Lesson
from lms.validators import DescriptionValidator, UrlValidator


class LessonSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Lesson
    Отображаются поля:
        id(int): Уникальный идентификатор урока.
        title(str): Название урока.
        description(str): Описание урока.
        preview(ImageField): Превью урока.
        video_url(URLField): Ссылка на видео урока.
        courses(ForeignKey): Внешний ключ на курс.
    """

    class Meta:
        model = Lesson
        exclude = ['owner']
        validators = [
            DescriptionValidator(field="description"),
            UrlValidator(field="video_url")
        ]


class CourseSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Course
    Отображаются поля:
        id(int): Уникальный идентификатор курса.
        count_lessons(int): Количество уроков в курсе
        lessons(list): Список уроков (LessonSerializer)
        title(str): Название курса.
        preview(ImageField): Превью курса.
        description(str): Описание курса.
    Методы:
        get_count_lessons(self, obj) -> int:
            Получение количества уроков в курсе
    """

    count_lessons = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        exclude = ['owner']
        validators = [DescriptionValidator(field="description")]

    def get_count_lessons(self, obj) -> int:
        """
        Получение количества уроков в курсе
        :param obj: Экземпляр курса
        :return: Количество уроков в курсе
        """
        count_lessons = obj.lessons.count()
        return count_lessons if count_lessons else 0
