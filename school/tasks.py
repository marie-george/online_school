from celery import shared_task
from django.core.mail import send_mail
from datetime import datetime, timedelta

from config import settings
from school.models import Subscription
from users.models import User


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


@shared_task
def check_user():

    now_date = datetime.now()
    one_month_ago = now_date - timedelta(days=30)
    inactive_users = User.objects.filter(last_login__lt=one_month_ago)
    inactive_users.update(is_active=False)
    print(inactive_users)
