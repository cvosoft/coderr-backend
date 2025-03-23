from rest_framework.pagination import PageNumberPagination

class ResultsSetPagination(PageNumberPagination):
    page_size = 6 # siehe frontend config.js
    page_size_query_param = 'page_size'
    max_page_size = 1000
    