from school.apps import SchoolConfig
from django.urls import path
from rest_framework.routers import DefaultRouter

from school.views import CourseViewSet, LessonCreateAPIView, LessonUpdateAPIView, LessonDestroyAPIView, \
    LessonListAPIView, LessonRetrieveAPIView, PaymentListAPIView

app_name = SchoolConfig.name

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')

urlpatterns = [
    path('lessons/create/', LessonCreateAPIView.as_view(), name='lesson-create'),
    path('lessons/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson-update'),
    path('lessons/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='lesson-delete'),
    path('lessons/', LessonListAPIView.as_view(), name='lesson-list'),
    path('lessons/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson-detail'),
    path('payments/', PaymentListAPIView.as_view(), name='payment-list')
] + router.urls
