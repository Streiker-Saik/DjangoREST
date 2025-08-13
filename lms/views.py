from django.db.models import QuerySet
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import (CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView,
                                     get_object_or_404)
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from lms.models import Course, Lesson, Subscription
from lms.paginators import LmsPaginator
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
    queryset = Course.objects.all().order_by("id")
    pagination_class = LmsPaginator

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

    @swagger_auto_schema(operation_description="Представление для получения списка всех курсов.")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Представление для получения курса.")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Представление для создания нового курса")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Представление для полного обновления курса по идентификатору")
    def update(self, request, *args, **kwargs):
        return super().update(request,*args, **kwargs)

    @swagger_auto_schema(operation_description="Представление для частичного обновления курса по идентификатору")
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Представление для удаления курса.")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

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

    # permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        operation_id="manager_subscribe",
        manual_parameters=[],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'course_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID курса для подписки"),
            },
            required=['course_id'],
        ),
        responses={
            200: openapi.Response('', openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING, description="Сообщение о результате операции"),
                },
            )),
            404: 'Курс не найден',
        }
    )
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

    @swagger_auto_schema(operation_id="lessons_create")
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


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
    # queryset = Lesson.objects.all().order_by('id')
    permission_classes = (IsAuthenticated,)
    pagination_class = LmsPaginator

    @swagger_auto_schema(operation_id="lessons_list")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet:
        """
        Возвращает список курсов, к которым у пользователя есть доступ.
        Если пользователь является модератором, возвращает все курсы.
        В противном случае, возвращает только курсы, принадлежащие пользователю.
        """
        user = self.request.user
        if user.is_authenticated:
            if user.groups.filter(name="Moderators").exists():
                return Lesson.objects.all().order_by("id")
            return Lesson.objects.filter(owner=user).order_by("id")
        return Lesson.objects.none()


class LessonRetrieveAPIView(RetrieveAPIView):
    """Представление для получения урока по идентификатору (GET)"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (
        IsAuthenticated,
        IsModerator | IsOwner,
    )

    @swagger_auto_schema(operation_id="lessons_read")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class LessonUpdateAPIView(UpdateAPIView):
    """Представление для обновления урока по идентификатору (PUT/PATH)"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (
        IsAuthenticated,
        IsModerator | IsOwner,
    )

    @swagger_auto_schema(
        operation_description="Полное обновление урока",
        operation_id="lessons_update"
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Частичное обновление урока",
        operation_id="lessons_partial_update"
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

class LessonDestroyAPIView(DestroyAPIView):
    """Представление для удаления урока по идентификатору (DELETE)"""

    queryset = Lesson.objects.all()
    permission_classes = (
        IsAuthenticated,
        ~IsModerator | IsOwner,
    )

    @swagger_auto_schema(operation_id="lessons_delete")
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
