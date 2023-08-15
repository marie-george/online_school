from rest_framework import viewsets, generics, filters
from rest_framework.permissions import IsAuthenticated

from school.models import Course, Lesson, Payment
from school.permissions import IsOwner, IsModerator
from school.serializers import CourseSerializer, LessonSerializer, PaymentSerializer


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]

    def perform_create(self, serializer):
        new_course = serializer.save()
        new_course.owner = self.request.user
        new_course.save()


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['course__name', 'payment_method']
    ordering_fields = ['payment_date']


# сортировка по дате оплаты:
#   прямой порядок - http://localhost:8000/school/payments/?ordering=payment_date
#   обратный порядок - http://localhost:8000/school/payments/?ordering=-payment_date

# фильтрация по НАЗВАНИЮ курса:
# http://localhost:8000/school/payments/?search=Modern England (вместо "Modern England" подставить свое)

# фильтрация по способу оплаты:
# http://localhost:8000/school/payments/?search=cash
# http://localhost:8000/school/payments/?search=bank_transfer

