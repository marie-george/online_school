from celery import shared_task
from django.core.mail import send_mail

from config import settings
from school.models import Subscription


@shared_task
def course_update_notification(object_pk):
    subscription_list = Subscription.objects.filter(course=object_pk)
    for i in subscription_list:
        send_mail(
            subject='Обновление материалов курса',
            message=f'Материал курсов был обновлен. Зайдите на наш сайт',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[i.user.email]
        )