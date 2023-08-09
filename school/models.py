from django.db import models

NULLABLE = {'null': True, 'blank': True}


class Course(models.Model):
    name = models.CharField(max_length=150, verbose_name='название')
    preview = models.ImageField(upload_to='courses/', verbose_name='превью', **NULLABLE)
    description = models.TextField(verbose_name='описание')


class Lesson(models.Model):
    name = models.CharField(max_length=150, verbose_name='название')
    preview = models.ImageField(upload_to='lessons/', verbose_name='превью', **NULLABLE)
    description = models.TextField(verbose_name='описание')
    link_to_video = models.CharField(max_length=150, verbose_name='ссылка на видео')