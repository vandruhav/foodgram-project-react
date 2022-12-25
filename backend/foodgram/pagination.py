"""Пагинация проекта 'foodgram'."""
from rest_framework.pagination import PageNumberPagination


class LimitPageNumberPagination(PageNumberPagination):
    """Пагинатор, наследуемый от PageNumberPagination."""

    page_size_query_param = 'limit'
