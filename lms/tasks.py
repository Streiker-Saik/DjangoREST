from celery import shared_task
from django.core.mail import send_mail
import smtplib
from config import settings
from lms.models import Course, Subscription


@shared_task
def send_course_update(course_id: int) -> None:
    """
    Отправление уведомления при обновлении курса подписчикам.
    :param course_id: ID курса
    """

    course = Course.objects.filter(pk=course_id).first()
    if not course:
        print(f"Курс с ID: {course_id} - не найден")

    subscribers = Subscription.objects.filter(course=course_id)

    for user in subscribers:
        email = user.email
        try:
            send_mail(
                subject="Курс был обновлен",
                message=f"Курс {course.title} был обновлен!",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email]
            )
        except smtplib.SMTPException as exc_info:
            print(f"{email}: {str(exc_info)}")
        else:
            print(f"{email}: Сообщение отправлено")
