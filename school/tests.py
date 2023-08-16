from rest_framework import status
from django.urls import reverse
from school.models import Course, Lesson, Subscription
from users.models import User
from rest_framework.test import APITestCase, APIClient


class LessonsTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            email='user@mail.ru',
            first_name='test',
            last_name='test',
            is_staff=False,
            is_superuser=False
        )

        self.user.set_password('123')
        self.user.save()
        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(
            name='test_course',
            description='test_course',
            owner=self.user
        )

        self.lesson = Lesson.objects.create(
            course=self.course,
            name='test_lesson',
            description='test_lesson',
            link_to_video='youtube.com',
            owner=self.user
        )

    def test_get_list(self):
        """Проверка получения списка уроков"""

        response = self.client.get(reverse('school:lesson-list'))

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {'count': 1,
             'next': None,
             'previous': None,
             'results': [
                 {'id': self.lesson.id,
                  'name': self.lesson.name,
                  'preview': None,
                  'description': self.lesson.description,
                  'link_to_video': self.lesson.link_to_video,
                  'course': self.lesson.course_id,
                  'owner': self.lesson.owner_id}
             ]
             }
        )

    def test_lesson_create(self):
        """Проверка создания урока"""

        response1 = self.client.post(
            reverse('school:lesson-create'),
            data={
                'course': self.course.id,
                'name': 'test_lesson_2',
                'description': 'test_lesson_2',
                'link_to_video': 'youtube.com',
                'owner': self.user.id
            }
        )

        self.assertEqual(
            response1.status_code,
            status.HTTP_201_CREATED
        )

        response2 = self.client.post(
            reverse('school:lesson-create'),
            data={
                'course': self.course.id,
                'name': 'test_lesson_3',
                'description': 'test_lesson_3',
                'link_to_video': 'google.com',
                'owner': self.user.id
            }
        )

        self.assertEqual(
            response2.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            Lesson.objects.all().count(),
            2
        )

    def test_get_lesson(self):
        """Проверка получения отдельного урока"""

        response = self.client.get(f'/school/lessons/{self.lesson.id}/')

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {
                'id': self.lesson.id,
                'name': self.lesson.name,
                'preview': None,
                'description': self.lesson.description,
                'link_to_video': self.lesson.link_to_video,
                'course': self.lesson.course_id,
                'owner': self.lesson.owner_id
            }
        )

    def test_lesson_update(self):
        """Проверка редактирования урока"""

        response = self.client.put(
            f'/school/lessons/update/{self.lesson.id}/',
            data={
                'course': self.course.id,
                'name': 'test_lesson_4',
                'description': 'test_lesson_4',
                'link_to_video': 'youtube.com',
                'owner': self.user.id
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_lesson_delete(self):
        """Проверка удаления урока"""

        response = self.client.delete(f'/school/lessons/delete/{self.lesson.id}/')

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertEqual(
            Lesson.objects.all().count(),
            0
        )


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            email='user@mail.ru',
            first_name='test',
            last_name='test',
            is_staff=False,
            is_superuser=False
        )

        self.user.set_password('123')
        self.user.save()
        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(
            name='test_course',
            description='test_course',
            owner=self.user
        )

        self.subscription = Subscription.objects.create(
            course=self.course,
            status=True,
            user=self.user
        )

    def test_subscription_create(self):
        """Проверка создания подписки"""

        response = self.client.post(
            reverse('school:subscription_create'),
            data={
                'course': self.course.id,
                'status': True,
                'user': self.user.id
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            Subscription.objects.all().count(),
            2
        )

    def test_subscription_update(self):
        """Проверка редактирования урока"""

        response = self.client.put(
            f'/school/subscription/update/{self.subscription.id}/',
            data={
                'course': self.course.id,
                'status': True,
                'user': self.user.id
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_course_has_subscription(self):
        """Проверка наличия у курса подписки"""
        response = self.client.get('/school/courses/')
        self.assertEqual(response.json()['results'][0]['subscription_status'], self.subscription.status)