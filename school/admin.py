from django.contrib import admin

from school.models import Course, Lesson, Payment


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'owner')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'owner')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'payment_date', 'course', 'amount', 'payment_method')

