from rest_framework import serializers

from school.models import Course, Lesson, Payment, Subscription
from school.validators import LinkValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [LinkValidator(field='link_to_video')]


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True, source='lesson_set')
    subscription_status = serializers.SerializerMethodField()

    def get_lessons_count(self, lesson):
        lessons = Lesson.objects.filter(course=lesson).all()
        if lessons:
            return lessons.count()
        return 0

    def get_subscription_status(self, instance):
        user = self.context['request'].user.id
        sub = Subscription.objects.filter(course=instance).filter(user=user)
        if sub:
            return sub.first().status
        return False

    class Meta:
        model = Course
        fields = (
            'name',
            'preview',
            'description',
            'lessons_count',
            'lessons',
            'owner',
            'subscription_status'
        )


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"


class PaymentIntentCreateSerializer(serializers.Serializer):
    course_id = serializers.PrimaryKeyRelatedField(source='course', queryset=Course.objects.all())


class PaymentMethodCreateSerializer(serializers.Serializer):
    payment_intent_id = serializers.CharField(max_length=500)
    payment_token = serializers.CharField(max_length=255)

    def validate(self, value):
        payment_intent_id = value['payment_intent_id']
        payment = Payment.objects.get(payment_intent_id=payment_intent_id)
        if payment is None:
            raise serializers.ValidationError(f"Платеж с ID {payment_intent_id} не найден")
        if payment.confirmation:
            raise serializers.ValidationError(f"Платеж с ID {payment_intent_id} уже подтвержден")
        return value


class PaymentIntentConfirmSerializer(serializers.Serializer):
    payment_intent_id = serializers.CharField(max_length=500)

    def validate(self, value):

        payment_intent_id = value['payment_intent_id']
        payment = Payment.objects.get(payment_intent_id=payment_intent_id)
        if payment is None:
            raise serializers.ValidationError(f"Платеж с ID {payment_intent_id} не найден")
        if payment.payment_method_id is None:
            raise serializers.ValidationError(f"К платежу с ID {payment_intent_id} не привязан метод платежа")
        if payment.confirmation:
            raise serializers.ValidationError(f"Платеж с ID {payment_intent_id} уже подтвержден")
        return value
