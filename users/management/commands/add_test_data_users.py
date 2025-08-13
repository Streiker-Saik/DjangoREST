from django.core.management import call_command
from django.core.management.base import BaseCommand

from users.models import Payment, User, TransactionStripe


class Command(BaseCommand):
    """Команда для добавления тестовых данных(пользователи, платежи, транзакции) из fixture"""

    help = "Add test data(user, payment, transaction_stripe) to the database"

    def handle(self, *args, **options) -> None:
        """Обрабатывает команду для добавления тестовых в базу данных"""
        # Удаляем все существующие
        User.objects.all().delete()
        Payment.objects.all().delete()
        TransactionStripe.objects.all().delete()

        call_command(
            "loaddata",
            (
                "users/fixture/user_fixture.json",
                "users/fixture/payment_fixture.json",
                "users/fixture/transaction_fixture.json",
            ),
        )
        self.stdout.write(self.style.SUCCESS("Успешно загружены данные из фикстуры"))
