from django.core.management import call_command
from django.core.management.base import BaseCommand

from lms.models import Course, Lesson


class Command(BaseCommand):
    """Команда для добавления тестовых данных(курсы, уроки) из fixture"""

    help = "Add test data(curse, lesson) to the database"

    def handle(self, *args, **options) -> None:
        """Обрабатывает команду для добавления тестовых данных в базу данных"""
        # Удаляем все существующие
        Course.objects.all().delete()
        Lesson.objects.all().delete()

        call_command(
            "loaddata",
            (
                "lms/fixture/course_fixture.json",
                "lms/fixture/lesson_fixture.json",
            ),
        )
        self.stdout.write(self.style.SUCCESS("Успешно загружены данные из фикстуры"))
