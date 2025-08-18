from celery import shared_task
from django.core.mail import send_mail
import smtplib
from config import settings
from lms.models import Course, Subscription
import logging


logger = logging.getLogger(__name__)

@shared_task
def send_course_update(course_id: int) -> None:
    """
    Отправление уведомления при обновлении курса подписчикам.
    :param course_id: ID курса
    """
    logger.info("Рассылка запущена")
    course = Course.objects.filter(pk=course_id).first()
    if not course:
        logger.warning(f"Курс с ID:{course_id} - не найден")
        return

    subscribers = Subscription.objects.filter(course=course_id)
    logger.info(f"Подписчиков: {len(subscribers)}")

    for subscription in subscribers:
        try:
            email = subscription.user.email
            try:
                send_mail(
                    subject="Курс был обновлен",
                    message=f"Курс {course.title} был обновлен!",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email]
                )
                logger.info(f"{email} - Ok")
            except smtplib.SMTPException as exc_info:
                logger.warning(str(exc_info))
        except Exception as exc_info:
            logger.error(str(exc_info))


