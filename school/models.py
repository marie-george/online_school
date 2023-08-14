from django.db import models

from config import settings

NULLABLE = {'null': True, 'blank': True}


class Course(models.Model):
    name = models.CharField(max_length=150, verbose_name='название')
    preview = models.ImageField(upload_to='courses/', verbose_name='превью', **NULLABLE)
    description = models.TextField(verbose_name='описание')


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete = models.CASCADE)
    name = models.CharField(max_length=150, verbose_name='название')
    preview = models.ImageField(upload_to='lessons/', verbose_name='превью', **NULLABLE)
    description = models.TextField(verbose_name='описание')
    link_to_video = models.CharField(max_length=150, verbose_name='ссылка на видео')


class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='пользователь')
    payment_date = models.DateField(verbose_name='дата оплаты')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    sum = models.IntegerField(verbose_name='сумма оплаты')
    payment_methods = (
        ('cash', 'наличные'),
        ('bank_transfer', 'перевод на счет'),
    )
    payment_method = models.CharField(choices=payment_methods, verbose_name='способ оплаты')