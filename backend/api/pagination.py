from rest_framework.pagination import PageNumberPagination
from .constants import MAX_PAGE_SIZE


class StandardResultsSetPagination(PageNumberPagination):
    page_size_query_param = "limit"
    max_page_size = MAX_PAGE_SIZE
