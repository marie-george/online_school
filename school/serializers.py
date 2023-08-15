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

    def get_subscribtion_status(self, instance):
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
            'owner'
        )


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"