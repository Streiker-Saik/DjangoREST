from django.db.models import QuerySet
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, \
    get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from lms.models import Course, Lesson, Subscription
from lms.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModerator, IsOwner


class CourseViewSet(ModelViewSet):
    """
    Представление набора действий для модели Course.
    Позволяет выполнять операции с курсами:
        отображение списка, создание, отображение, полное обновление, частичное обновление, удаление.
    Методы:
        get_queryset(self) -> QuerySet: - временно отключена.
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
    queryset = Course.objects.all()

    # def get_queryset(self) -> QuerySet:
    #     """
    #     Возвращает список уроков, к которым у пользователя есть доступ.
    #     Если пользователь является модератором, возвращает все уроки.
    #     В противном случае, возвращает только уроки, принадлежащие пользователю.
    #     """
    #     user = self.request.user
    #     if user.is_authenticated:
    #         if user.groups.filter(name="Moderators").exists():
    #             return Course.objects.all()
    #         return Course.objects.filter(owner=user)
    #     return Course.objects.none()

    def get_permissions(self) -> list:
        """Определяет права доступа для различных действий."""
        if self.action == "create":
            self.permission_classes = [IsAuthenticated, ~IsModerator]
        elif self.action in ["retrieve", "update", "partial_update"]:
            self.permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        elif self.action == "destroy":
            self.permission_classes = [IsAuthenticated, ~IsModerator | IsOwner]

        return super().get_permissions()

    def perform_create(self, serializer) -> None:
        """Сохраняет новый урок с текущим пользователем как владельцем."""
        new_course = serializer.save()
        new_course.owner = self.request.user
        new_course.save()


class ManageSubscriptionAPIView(APIView):
    """
    Представление для создания/удаления подписки
    Методы:
        post(self, request: Request) -> Response:
            Пост запрос на добавление или удаление подписки
    """

    def post(self, request: Request) -> Response:
        """Пост запрос на добавление(если подписки нет) или удаление подписки(если есть)."""
        user = request.user
        course = request.data.get("course_id")
        course_item = get_object_or_404(Course, id=course)

        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = "подписка удалена"
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = "подписка добавлена"
        return Response({"message": message})


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
