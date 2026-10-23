from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from course.models import Course, Lesson

from .models import Activity


class ActivityTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='student@example.com', password='Password123!')
        self.course = Course.objects.create(
            title='Algorithms',
            slug='algorithms',
            created_by=self.user,
            status=Course.PUBLISHED,
        )
        self.lesson = Lesson.objects.create(
            course=self.course,
            title='Sorting',
            slug='sorting',
            status=Lesson.PUBLISHED,
        )
        self.client.force_authenticate(user=self.user)

    def test_track_started_and_mark_as_done_and_str(self):
        resp = self.client.post(f'/api/v1/activities/track_started/{self.course.slug}/{self.lesson.slug}/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['status'], Activity.STARTED)

        activity = Activity.objects.get(course=self.course, lesson=self.lesson, created_by=self.user)
        self.assertIsInstance(str(activity), str)

        active_resp = self.client.get('/api/v1/activities/get_active_courses/')
        self.assertEqual(active_resp.status_code, 200)
        self.assertEqual(len(active_resp.data), 1)

        done_resp = self.client.post(f'/api/v1/activities/mark_as_done/{self.course.slug}/{self.lesson.slug}/')
        self.assertEqual(done_resp.status_code, 200)
        self.assertEqual(done_resp.data['status'], Activity.DONE)
