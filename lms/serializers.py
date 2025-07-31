from rest_framework.serializers import ModelSerializer, SerializerMethodField

from lms.models import Course, Lesson


class CourseSerializer(ModelSerializer):
    """
    Сериализатор для модели Course
    Отображаются поля:
        id(int): Уникальный идентификатор курса.
        count_lessons(int): Количество уроков в курсе
        title(str): Название курса.
        preview(ImageField): Превью курса.
        description(str): Описание курса.
    Методы:
        get_count_lessons(self, obj) -> int:
            Получение количества уроков в курсе
    """
    count_lessons = SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"

    def get_count_lessons(self, obj) -> int:
        """
        Получение количества уроков в курсе
        :param obj: Экземпляр курса
        :return: Количество уроков в курсе
        """
        count_lessons = len(obj.lessons.all())
        return count_lessons if count_lessons else 0


class LessonSerializer(ModelSerializer):
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
        fields = "__all__"
