from typing import Optional

import stripe
from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY

class TransactionStripeService:
    """
    Сервис работы с Strip транзакциями
    Методы:
        get_strip_product(product_name: str) -> dict:
            Получение продукта из Strip
        create_strip_course(product_name: str) -> dict:
            Создание продукта в Strip
        search_strip_product(product_name: str) -> Optional[dict]:
            Поиск продукта по названию в Strip
        get_strip_price(amount: int, product_id: str) -> dict:
            Получение цены из Strip
        create_strip_price(amount: int, product_id: str) -> dict:
            Создание цены в Strip
        search_strip_price(product_id: str) -> Optional[dict]:
            Поиск продукта по названию в Strip
        create_strip_session(price: dict) -> tuple:
            Создание сессии в Strip
        check_status(transaction: dict) -> str:
            Проверка статуса платежа в Strip
    """

    @staticmethod
    def get_strip_product(product_name: str) -> dict:
        """Получение продукта из Strip"""
        product = TransactionStripeService.search_strip_product(product_name)
        if not product:
            return TransactionStripeService.create_strip_course(product_name)
        return product

    @staticmethod
    def create_strip_course(product_name: str) -> dict:
        """Создание продукта в Strip"""
        product = stripe.Product.create(name=product_name)
        return product

    @staticmethod
    def search_strip_product(product_name: str) -> Optional[dict]:
        """Поиск продукта по названию в Strip"""
        products = stripe.Product.search(
            query=f"active:'true' AND name: '{product_name}'",
        )
        return products.data[0] if products.data else None

    @staticmethod
    def get_strip_price(amount: int, product_id: str) -> dict:
        """Получение цены из Strip"""
        price = TransactionStripeService.search_strip_price(product_id)
        if not price:
            return TransactionStripeService.create_strip_price(amount, product_id)
        return price

    @staticmethod
    def create_strip_price(amount: int, product_id: str) -> dict:
        """Создание цены в Strip"""
        price = stripe.Price.create(
            currency="rub",
            unit_amount=amount * 100,
            product=product_id,
        )
        return price

    @staticmethod
    def search_strip_price(product_id: str) -> Optional[dict]:
        """Поиск продукта по названию в Strip"""
        price = stripe.Price.search(
            query=f"active:'true' AND product: '{product_id}'",
        )
        return price.data[0] if price.data else None

    @staticmethod
    def create_strip_session(price: dict) -> tuple:
        """Создание сессии в Strip"""
        session = stripe.checkout.Session.create(
            success_url="http://127.0.0.1:8000/",
            line_items=[{"price": price.get("id"), "quantity": 1}],
            mode="payment",
        )
        return session.get("id"), session.get("url")

    @staticmethod
    def retrieve_strip_session(strip_pay_id: str) -> dict:
        """Получение данных о сессии в Strip"""
        session = stripe.checkout.Session.retrieve(strip_pay_id)
        return session


