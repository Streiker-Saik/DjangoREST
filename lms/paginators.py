from rest_framework.pagination import PageNumberPagination


class LmsPaginator(PageNumberPagination):
    """
    Пагинатор для приложения lms
    К-во элементов 3 (максимум 10) на странице
    """

    page_size = 3
    page_size_query_param = "page_size"
    max_page_size = 10
