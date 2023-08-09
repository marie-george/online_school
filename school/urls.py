from school.apps import SchoolConfig
from django.urls import path
from rest_framework.routers import DefaultRouter

from school.views import CourseViewSet

app_name = SchoolConfig.name

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')

urlpatterns = [

] + router.urls
