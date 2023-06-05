from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    ''' This class is used for custom pagination '''
    page_size = 5
