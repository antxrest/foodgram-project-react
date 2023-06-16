from rest_framework.pagination import PageNumberPagination


class LimitPaginator(PageNumberPagination):
    """Класс пагинации страниц."""
    page_size_query_param = 'limit'
