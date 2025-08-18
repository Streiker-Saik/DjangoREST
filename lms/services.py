import datetime

from django.utils import timezone

from lms.models import Course
from lms.tasks import send_course_update


class CourseServices:
    """
    Сервис работы с курсами
    Методы:
        send_notif(course: Course) -> None:
            Отправка уведомлений если прошло больше 4 часов после последнего изменения
    """

    @staticmethod
    def send_notif(course: Course) -> None:
        """Отправка уведомлений если прошло больше 4 часов после последнего изменения"""
        if timezone.now() - course.update_at > datetime.timedelta(hours=4):
            send_course_update.delay(course_id=course.pk)
