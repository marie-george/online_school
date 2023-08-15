from rest_framework import serializers

from school.models import Course, Lesson, Payment
from school.validators import LinkValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [LinkValidator(field='link_to_video')]


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True, source='lesson_set')

    def get_lessons_count(self, lesson):
        lessons = Lesson.objects.filter(course=lesson).all()
        if lessons:
            return lessons.count()
        return 0

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