from django.contrib.auth.models import Group
from django.db import connection
from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Course, Lesson, Subscription
from users.models import User


class LmsLessonTestCase(APITestCase):

    def setUp(self):
        # Сброс счетчиков до 1
        with connection.cursor() as cursor:
            cursor.execute("ALTER SEQUENCE lms_course_id_seq RESTART WITH 1;")
            cursor.execute("ALTER SEQUENCE lms_lesson_id_seq RESTART WITH 1;")
        # Создание пользователя и ацетификация
        self.user = User.objects.create(email="test@test.com")
        self.client.force_authenticate(user=self.user)
        # Заполнение тестовым курсом и уроком БД
        self.course = Course.objects.create(title="Python-разработчик", owner=self.user)
        self.lesson = Lesson.objects.create(title="1. Основы алгоритмизации", courses=self.course, owner=self.user)

    def test_list_lesson(self):
        """Тестирование просмотра списка уроков"""
        response = self.client.get(f"/courses/lessons/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.json(),
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": self.lesson.pk,
                        "title": "1. Основы алгоритмизации",
                        "description": None,
                        "preview": None,
                        "video_url": None,
                        "courses": self.course.pk,
                    }
                ],
            },
        )

    def test_list_lesson_is_moderator(self):
        """Тестирование просмотра списка уроков от имена модератора"""
        Lesson.objects.create(title="Тестовый урок", courses=self.course, owner=None)
        group = Group.objects.create(name="Moderators")
        self.user.groups.add(group)
        self.client.force_authenticate(user=self.user)

        response = self.client.get(f"/courses/lessons/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.json(),
            {
                "count": 2,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": self.lesson.pk,
                        "title": "1. Основы алгоритмизации",
                        "description": None,
                        "preview": None,
                        "video_url": None,
                        "courses": self.course.pk,
                    },
                    {
                        "id": 2,
                        "title": "Тестовый урок",
                        "description": None,
                        "preview": None,
                        "video_url": None,
                        "courses": self.course.pk,
                    },
                ],
            },
        )

    def test_retrieve_lesson(self):
        """Тестирование просмотра урока"""

        response = self.client.get(f"/courses/lessons/{self.lesson.pk}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.json(),
            {
                "id": self.lesson.pk,
                "title": "1. Основы алгоритмизации",
                "description": None,
                "preview": None,
                "video_url": None,
                "courses": self.course.pk,
            },
        )

    def test_create_lesson(self):
        """Тестирование создание урока"""
        data = {"title": "2.1 Типы данных", "courses": self.course.pk, "owner": self.user.pk}
        response = self.client.post("/courses/lessons/create/", data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(
            response.json(),
            {
                "id": 2,
                "title": "2.1 Типы данных",
                "description": None,
                "preview": None,
                "video_url": None,
                "courses": self.course.pk,
            },
        )

    def test_create_lesson_invalid_description(self):
        """Тестирование создание урока, со сторонней ссылкой в описании"""
        data = {
            "title": "2.1 Типы данных",
            "description": "Здесь учат http://sky.pro/",
            "courses": self.course.pk,
            "owner": self.user.pk,
        }
        response = self.client.post("/courses/lessons/create/", data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "В тексе присутствует сторонняя ссылка (не на YouTube)",
            response.data.get("non_field_errors"),
        )

    def test_create_lesson_invalid_url(self):
        """Тестирование создание урока, со сторонней ссылкой"""
        data = {
            "title": "2.1 Типы данных",
            "video_url": "http://sky.pro/",
            "courses": self.course.pk,
            "owner": self.user.pk,
        }
        response = self.client.post("/courses/lessons/create/", data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "Можно прикреплять только ссылки видео на YouTube",
            response.data.get("non_field_errors"),
        )

    def test_update_lesson(self):
        """Тестирование обновления урока"""
        data = {"title": "Изменили", "description": "Изменили", "courses": self.course.pk}
        response = self.client.put(f"/courses/lessons/{self.lesson.pk}/update/", data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.json(),
            {
                "id": self.lesson.pk,
                "title": "Изменили",
                "description": "Изменили",
                "preview": None,
                "video_url": None,
                "courses": self.course.pk,
            },
        )

    def test_partial_update_lesson(self):
        """Тестирование частичного обновления урока"""
        data = {"description": "Изменили"}
        response = self.client.patch(f"/courses/lessons/{self.lesson.pk}/update/", data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.json(),
            {
                "id": self.lesson.pk,
                "title": "1. Основы алгоритмизации",
                "description": "Изменили",
                "preview": None,
                "video_url": None,
                "courses": self.course.pk,
            },
        )

    def test_destroy_lesson(self):
        """Тестирование удаление урока"""

        response = self.client.delete(f"/courses/lessons/{self.lesson.pk}/delete/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(Lesson.objects.all().exists())


class LmsCourseTestCase(APITestCase):
    """"""

    def setUp(self):
        with connection.cursor() as cursor:
            cursor.execute("ALTER SEQUENCE lms_course_id_seq RESTART WITH 1;")
            cursor.execute("ALTER SEQUENCE lms_lesson_id_seq RESTART WITH 1;")
        # Создание пользователя и ацетификация
        self.user = User.objects.create(email="test@test.com")
        self.client.force_authenticate(user=self.user)
        # Заполнение тестовым курсом и уроком БД
        self.course = Course.objects.create(title="Python-разработчик", owner=self.user)

    def test_list_courses(self):
        """Тестирование просмотра списка курсов"""
        response = self.client.get(f"/courses/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.json(),
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": 1,
                        "count_lessons": 0,
                        "lessons": [],
                        "is_subscribed": False,
                        "title": "Python-разработчик",
                        "preview": None,
                        "description": None,
                    }
                ],
            },
        )

    def test_create_course(self):
        """Тестирование создание урока"""
        data = {"title": "Java-разработчик", "owner": self.user.pk}
        response = self.client.post("/courses/", data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(
            response.json(),
            {
                "id": 2,
                "count_lessons": 0,
                "lessons": [],
                "is_subscribed": False,
                "title": "Java-разработчик",
                "preview": None,
                "description": None,
            },
        )

    def test_update_course(self):
        """Тестирование обновления курса"""
        data = {"title": "Изменили", "description": "Изменили", "courses": self.course.pk}
        response = self.client.put(f"/courses/{self.course.pk}/", data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.json(),
            {
                "id": self.course.pk,
                "count_lessons": 0,
                "lessons": [],
                "is_subscribed": False,
                "title": "Изменили",
                "preview": None,
                "description": "Изменили",
            },
        )

    def test_partial_update_course(self):
        """Тестирование частичного обновления курса"""
        data = {"description": "Изменили"}
        response = self.client.patch(f"/courses/{self.course.pk}/", data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.json(),
            {
                "id": self.course.pk,
                "count_lessons": 0,
                "lessons": [],
                "is_subscribed": False,
                "title": "Python-разработчик",
                "preview": None,
                "description": "Изменили",
            },
        )

    def test_destroy_course(self):
        """Тестирование удаление курса"""

        response = self.client.delete(f"/courses/{self.course.pk}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(Course.objects.all().exists())


class LmsSubscriptionTestCase(APITestCase):
    """"""

    def setUp(self):
        self.user = User.objects.create(email="test@test.com")
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(title="Python-разработчик", owner=self.user)

    def test_create_subscription(self):
        """Тестирование создание подписки"""
        data = {"course_id": self.course.id}
        response = self.client.post("/courses/manger_subscribe/", data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(
            "подписка добавлена",
            response.data.get("message"),
        )
        self.assertTrue(Subscription.objects.all().exists())

    def test_delete_subscription(self):
        """Тестирование удаление подписки"""
        data = {"course_id": self.course.id}
        Subscription.objects.create(course=self.course, user=self.user)
        response = self.client.post("/courses/manger_subscribe/", data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(
            "подписка удалена",
            response.data.get("message"),
        )
        self.assertFalse(Subscription.objects.all().exists())


