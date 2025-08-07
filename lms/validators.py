import re

from rest_framework.validators import ValidationError


class DescriptionValidator:
    """Валидатор проверки описания на наличие ссылок"""

    def __init__(self, field) -> None:
        """
        Инициализатор валидатора.
        :param field: Имя поля для валидации
        """

        self.field = field

    def __call__(self, value: dict) -> None:
        """
        Проверяет значение на наличие ссылок кроме YouTube.
        :param value: Словарь, содержащий проверяемое значение
        :raise ValidationError: Если в тексе присутствует сторонняя ссылка
        """
        pattern_url = re.compile(r"https?://[^\s]+")
        pattern_url_youtube = re.compile(r"https?://(www\.)?youtube\.com/.*")
        tmp_value =dict(value).get(self.field)
        if not tmp_value:
            return
        all_url = pattern_url.findall(tmp_value)
        for url in all_url:
            if not bool(re.fullmatch(pattern_url_youtube, url)):
                raise ValidationError("В тексе присутствует сторонняя ссылка (не на YouTube)")


class UrlValidator:
    """Валидатор url ссылки"""

    def __init__(self, field: str) -> None:
        """
        Инициализатор валидатора.
        :param field: Имя поля для валидации
        """
        self.field = field

    def __call__(self, value: dict) -> None:
        """
        Проверяет значение на соответствие формату ссылки видео на YouTube.
        :param value: Словарь, содержащий проверяемое значение
        :raise ValidationError: Если ссылки не соответствуют формату видео ссылки YouTube.
        """
        pattern = re.compile(r"https?://(www\.)?youtube\.com/watch\?v=.*")
        tmp_value =dict(value).get(self.field)
        if tmp_value is None:
            return
        if not bool(re.fullmatch(pattern, tmp_value)):
            raise ValidationError("Можно прикреплять только ссылки видео на YouTube")