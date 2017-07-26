from rest_framework.pagination import PageNumberPagination

class ListStateSetPagination(PageNumberPagination):
    page_size = 32
    page_size_query_param = 'page_size'

class ListMunicipalitySetPagination(PageNumberPagination):
    page_size = 600
    page_size_query_param = 'page_size'

class ListRatePagination(PageNumberPagination):
    page_size = 56
    page_size_query_param = 'page_size'
