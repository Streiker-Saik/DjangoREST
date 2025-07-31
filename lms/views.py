from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.viewsets import ModelViewSet

from lms.models import Course, Lesson
from lms.serializers import CourseSerializer, LessonSerializer


class CourseViewSet(ModelViewSet):
    """
    Представление набора действий для модели Course.
    Позволяет выполнять операции с курсами:
        отображение списка, создание, отображение, полное обновление, частичное обновление, удаление.
    """

    serializer_class = CourseSerializer
    queryset = Course.objects.all()


class LessonCreateAPIView(CreateAPIView):
    """Представление для создания нового урока (POST)"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonListAPIView(ListAPIView):
    """Представление для получения списка всех уроков (GET)"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonRetrieveAPIView(RetrieveAPIView):
    """Представление для получения урока по идентификатору (GET)"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonUpdateAPIView(UpdateAPIView):
    """Представление для обновления урока по идентификатору (PUT/PATH)"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonDestroyAPIView(DestroyAPIView):
    """Представление для удаления урока по идентификатору (DELETE)"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
