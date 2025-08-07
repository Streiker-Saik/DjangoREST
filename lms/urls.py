from django.urls import path
from rest_framework.routers import DefaultRouter

from lms.apps import ImsConfig
from lms.views import (CourseViewSet, LessonCreateAPIView, LessonDestroyAPIView, LessonListAPIView,
                       LessonRetrieveAPIView, LessonUpdateAPIView, ManageSubscriptionAPIView)

app_name = ImsConfig.name

router = DefaultRouter()
router.register(r"", CourseViewSet, basename="course")

urlpatterns = [
    path("lessons/", LessonListAPIView.as_view(), name="lessons-list"),
    path("lessons/create/", LessonCreateAPIView.as_view(), name="lesson-create"),
    path("lessons/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lesson-detail"),
    path("lessons/<int:pk>/update/", LessonUpdateAPIView.as_view(), name="lesson-update"),
    path("lessons/<int:pk>/delete/", LessonDestroyAPIView.as_view(), name="lesson-delete"),

    path("manger_subscribe/", ManageSubscriptionAPIView.as_view(), name="manger-subscribe")
]
urlpatterns += router.urls
