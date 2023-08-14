from django.core.management import BaseCommand

from school.models import Payment, Course
from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        Payment.objects.all().delete()
        payment_list = [
            {'user': User(1), 'payment_date': '2023-08-15', 'course': Course(1), 'sum': '20000', 'payment_method': 'cash'},
            {'user': User(1), 'payment_date': '2023-08-13', 'course': Course(1), 'sum': '20000', 'payment_method': 'cash'},
            {'user': User(1), 'payment_date': '2023-08-12', 'course': Course(1), 'sum': '20000', 'payment_method': 'bank_transfer'},
            {'user': User(1), 'payment_date': '2023-08-10', 'course': Course(2), 'sum': '30000', 'payment_method': 'cash'},
            {'user': User(1), 'payment_date': '2023-08-09', 'course': Course(2), 'sum': '30000', 'payment_method': 'bank_transfer'},
        ]

        payment_objects = []
        for payment_item in payment_list:
            payment_objects.append(Payment(**payment_item))

        Payment.objects.bulk_create(payment_objects)