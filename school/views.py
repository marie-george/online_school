from rest_framework import viewsets

from school.models import Course, Lesson
from school.serializers import CourseSerializer


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

