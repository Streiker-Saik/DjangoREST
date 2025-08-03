from django.db.models import QuerySet
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from lms.models import Course, Lesson
from lms.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModerator, IsOwner


class CourseViewSet(ModelViewSet):
    """
    Представление набора действий для модели Course.
    Позволяет выполнять операции с курсами:
        отображение списка, создание, отображение, полное обновление, частичное обновление, удаление.
    Методы:
        get_queryset(self) -> QuerySet:
            Возвращает список уроков, к которым у пользователя есть доступ.
            Если пользователь является модератором, возвращает все уроки.
            В противном случае, возвращает только уроки, принадлежащие пользователю
        get_permissions(self) -> list:
            Определяет права доступа для различных действий:
                создание - авторизованные пользователи не являющиеся модераторами
                просмотр/изменение - авторизованные пользователи: модераторы и владельцы
                удаление - авторизованные пользователи: владельцы
        perform_create(self, serializer) -> None:
            Сохраняет новый урок с текущим пользователем как владельцем.
    """

    serializer_class = CourseSerializer

    def get_queryset(self) -> QuerySet:
        """
        Возвращает список уроков, к которым у пользователя есть доступ.
        Если пользователь является модератором, возвращает все уроки.
        В противном случае, возвращает только уроки, принадлежащие пользователю.
        """
        user = self.request.user
        if user.is_authenticated:
            if user.groups.filter(name="Moderators").exists():
                return Course.objects.all()
            return Course.objects.filter(owner=user)
        return Course.objects.none()

    def get_permissions(self) -> list:
        """Определяет права доступа для различных действий."""
        if self.action == "create":
            self.permission_classes = [IsAuthenticated, ~IsModerator]
        elif self.action in ["retrieve", "update"]:
            self.permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        elif self.action == "destroy":
            self.permission_classes = [IsAuthenticated, ~IsModerator | IsOwner]

        return super().get_permissions()

    def perform_create(self, serializer) -> None:
        """Сохраняет новый урок с текущим пользователем как владельцем."""
        new_course = serializer.save()
        new_course.owner = self.request.user
        new_course.save()


class LessonCreateAPIView(CreateAPIView):
    """
    Представление для создания нового урока (POST)
    Методы:
        perform_create(self, serializer) -> None:
            Сохраняет новый урок с текущим пользователем как владельцем.
    """

    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, ~IsModerator)

    def perform_create(self, serializer) -> None:
        """Сохраняет новый урок с текущим пользователем как владельцем."""
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonListAPIView(ListAPIView):
    """
    Представление для получения списка всех уроков (GET).
    Методы:
        get_queryset(self) -> QuerySet:
            Возвращает список курсов, к которым у пользователя есть доступ.
            Если пользователь является модератором, возвращает все курсы.
            В противном случае, возвращает только курсы, принадлежащие пользователю.
    """

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self) -> QuerySet:
        """
        Возвращает список курсов, к которым у пользователя есть доступ.
        Если пользователь является модератором, возвращает все курсы.
        В противном случае, возвращает только курсы, принадлежащие пользователю.
        """
        user = self.request.user
        if user.is_authenticated:
            if user.groups.filter(name="Moderators").exists():
                return Lesson.objects.all()
            return Lesson.objects.filter(owner=user)
        return Lesson.objects.none()


class LessonRetrieveAPIView(RetrieveAPIView):
    """Представление для получения урока по идентификатору (GET)"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsModerator | IsOwner,)


class LessonUpdateAPIView(UpdateAPIView):
    """Представление для обновления урока по идентификатору (PUT/PATH)"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsModerator | IsOwner,)


class LessonDestroyAPIView(DestroyAPIView):
    """Представление для удаления урока по идентификатору (DELETE)"""

    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, ~IsModerator | IsOwner,)
