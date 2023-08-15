from rest_framework.pagination import PageNumberPagination


class LessonPaginator(PageNumberPagination):
    page_size = 3


class CoursePaginator(PageNumberPagination):
    page_size = 3
