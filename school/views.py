from rest_framework.response import Response
from rest_framework import viewsets, generics, filters, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import APIException

from school.models import Course, Lesson, Payment, Subscription
from school.paginators import CoursePaginator, LessonPaginator
from school.permissions import IsOwner
from school.serializers import CourseSerializer, LessonSerializer, PaymentSerializer, SubscriptionSerializer, \
    PaymentIntentCreateSerializer, PaymentMethodCreateSerializer, PaymentIntentConfirmSerializer
from school.services import PaymentService
from users.models import UserRoles


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = CoursePaginator

    def perform_create(self, serializer):
        new_course = serializer.save()
        new_course.owner = self.request.user
        new_course.save()

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser or user.role == UserRoles.MODERATOR:
            return Course.objects.all()
        else:
            return Course.objects.filter(owner=user)


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
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser or user.role == UserRoles.MODERATOR:
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(owner=user)


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = LessonPaginator

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser or user.role == UserRoles.MODERATOR:
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(owner=user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser or user.role == UserRoles.MODERATOR:
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(owner=user)


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

class SubscriptionCreateAPIView(generics.CreateAPIView):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()
    permission_classes = [IsAuthenticated]


class SubscriptionUpdateView(generics.UpdateAPIView):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()
    permission_classes = [IsAuthenticated]


class StripeServiceError(APIException):
    status_code = 400
    default_detail = 'Ошибка сервиса оплаты'
    default_code = 'payment_error'


class PaymentIntentCreateView(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        serializer = PaymentIntentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            course = serializer.validated_data['course']
            user_id = request.user

            payment_intent = PaymentService.create_payment_intent(course, user_id)
            payment = Payment.objects.get(payment_intent_id=payment_intent['id'])
        except StripeServiceError as e:
            raise StripeServiceError(detail=str(e))

        except Payment.DoesNotExist:
            raise APIException(detail='Платеж не найден')
        else:
            data = PaymentSerializer(payment).data
            status_code = status.HTTP_201_CREATED

            return Response(data, status=status_code)


class PaymentMethodCreateView(generics.CreateAPIView):

    def post(self, request, *args, **kwargs):

        serializer = PaymentMethodCreateSerializer(data=request.data)
        if serializer.is_valid():
            payment_intent_id = serializer.validated_data['payment_intent_id']
            payment_token = serializer.validated_data['payment_token']
            try:
                PaymentService.connection(payment_intent_id, payment_token)
                payment = Payment.objects.get(payment_intent_id=payment_intent_id)
                payment_serializer = PaymentSerializer(payment)
                return Response(payment_serializer.data, status=status.HTTP_201_CREATED)
            except Exception as error:
                return Response({'error': str(error)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentIntentConfirmView(generics.CreateAPIView):

    def post(self, request, *args, **kwargs):

        serializer = PaymentIntentConfirmSerializer(data=request.data)
        if serializer.is_valid():
            payment_intent_id = serializer.validated_data['payment_intent_id']
            try:
                PaymentService.confirm_payment_intent(payment_intent_id)
                payment = Payment.objects.get(payment_intent_id=payment_intent_id)
                payment_serializer = PaymentSerializer(payment)
                return Response(payment_serializer.data, status=status.HTTP_201_CREATED)
            except Exception as error:
                return Response({"error": str(error)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
