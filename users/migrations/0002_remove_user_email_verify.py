# Generated by Django 4.2.4 on 2023-08-09 00:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='email_verify',
        ),
    ]