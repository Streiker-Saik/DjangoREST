import datetime
import logging

from celery import shared_task
from django.utils import timezone

from users.models import User


logger = logging.getLogger(__name__)

@shared_task
def deactivate_inactive_users() -> None:
    """Деактивация пользователей не активных 31 день"""
    logger.info("Запущена проверка неактивных пользователей")
    today = timezone.now()
    users = User.objects.filter(last_login__isnull=False, is_active=True, is_superuser=False)
    logger.info(f"Пользователей: {len(users)}")

    for user in users:
        try:
            logger.info(f"Проверка пользователя: {user.email}")
            last_login = user.last_login
            if today - last_login > datetime.timedelta(days=31):
                user.is_active = False
                user.save()
                logger.info(f"Пользователь: {user.email} - заблокирован")

        except Exception as exc_info:
            logger.error(str(exc_info))

    logger.info(f"Проверка завершена")

