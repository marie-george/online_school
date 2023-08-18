from django.db import models

from config import settings
from users.models import User

NULLABLE = {'null': True, 'blank': True}


class Course(models.Model):
    name = models.CharField(max_length=150, verbose_name='название')
    preview = models.ImageField(upload_to='courses/', verbose_name='превью', **NULLABLE)
    description = models.TextField(verbose_name='описание')
    price = models.IntegerField(default=0, verbose_name='цена курса')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True,
                              verbose_name='владелец')


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete = models.CASCADE)
    name = models.CharField(max_length=150, verbose_name='название')
    preview = models.ImageField(upload_to='lessons/', verbose_name='превью', **NULLABLE)
    description = models.TextField(verbose_name='описание')
    link_to_video = models.CharField(max_length=150, verbose_name='ссылка на видео')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='владелец')


class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='пользователь')
    payment_date = models.DateField(verbose_name='дата оплаты')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    amount = models.IntegerField(verbose_name='сумма оплаты')
    payment_methods = (
        ('cash', 'наличные'),
        ('bank_transfer', 'перевод на счет'),
    )
    payment_method = models.CharField(choices=payment_methods, verbose_name='способ оплаты')
    payment_intent_id = models.CharField(max_length=10, **NULLABLE, verbose_name='id намерения платежа')
    payment_method_id = models.CharField(max_length=10, **NULLABLE, verbose_name='id метода платежа')
    status = models.CharField(max_length=50, **NULLABLE, verbose_name='cтатус платежа')
    confirmation = models.BooleanField(default=False, verbose_name='подтверждение платежа')


class Subscription(models.Model):
    status = models.BooleanField(default=True, verbose_name='статус подписки')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс')

    class Meta:
        verbose_name = "подписка"
        verbose_name_plural = "подписки"