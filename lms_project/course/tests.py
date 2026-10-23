from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from .models import Category, Comment, Course, Lesson, Quiz


class CourseModelAndAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='instructor@example.com',
            password='StrongPassword123!',
            first_name='Ali',
            last_name='Valiyev',
        )
        self.category = Category.objects.create(title='Programming', slug='programming')
        self.course = Course.objects.create(
            title='Python Mastery',
            slug='python-mastery',
            short_description='Learn Python from scratch',
            long_description='Detailed Python course description',
            created_by=self.user,
            status=Course.PUBLISHED,
        )
        self.course.categories.add(self.category)

        self.lesson = Lesson.objects.create(
            course=self.course,
            title='Variables',
            slug='variables',
            short_description='Intro to variables',
            long_description='Full lesson content on variables',
            status=Lesson.PUBLISHED,
            lesson_type=Lesson.QUIZ,
        )
        self.draft_lesson = Lesson.objects.create(
            course=self.course,
            title='Secret Draft Lesson',
            slug='secret-draft',
            status=Lesson.DRAFT,
        )
        self.quiz = Quiz.objects.create(
            lesson=self.lesson,
            question='What is x = 5?',
            answer='Assignment',
            op1='Assignment',
            op2='Comparison',
            op3='Loop',
        )

    def test_model_str_representations_return_strings(self):
        self.assertEqual(str(self.category), 'Programming')
        self.assertEqual(str(self.course), 'Python Mastery')
        self.assertEqual(str(self.lesson), 'Variables')
        self.assertEqual(str(self.quiz), 'What is x = 5?')

    def test_public_endpoints_accessible_without_auth(self):
        resp_cats = self.client.get('/api/v1/courses/get_categories/')
        self.assertEqual(resp_cats.status_code, 200)
        self.assertEqual(len(resp_cats.data), 1)

        resp_courses = self.client.get('/api/v1/courses/')
        self.assertEqual(resp_courses.status_code, 200)
        self.assertEqual(len(resp_courses.data), 1)

        resp_invalid_cat = self.client.get('/api/v1/courses/?category_id=abc')
        self.assertEqual(resp_invalid_cat.status_code, 400)

    def test_course_detail_hides_draft_lessons_and_full_content_when_unauthenticated(self):
        resp = self.client.get(f'/api/v1/courses/{self.course.slug}/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.data['lessons']), 1)
        self.assertNotIn('long_description', resp.data['lessons'][0])

        self.client.force_authenticate(user=self.user)
        resp_auth = self.client.get(f'/api/v1/courses/{self.course.slug}/')
        self.assertEqual(resp_auth.status_code, 200)
        self.assertIn('long_description', resp_auth.data['lessons'][0])

    def test_comments_and_quiz_endpoints(self):
        self.client.force_authenticate(user=self.user)

        quiz_resp = self.client.get(f'/api/v1/courses/{self.course.slug}/{self.lesson.slug}/get-quiz/')
        self.assertEqual(quiz_resp.status_code, 200)
        self.assertEqual(quiz_resp.data['question'], 'What is x = 5?')

        comment_resp = self.client.post(
            f'/api/v1/courses/{self.course.slug}/{self.lesson.slug}/',
            {'name': 'Student', 'content': 'Great lesson!'},
            format='json',
        )
        self.assertEqual(comment_resp.status_code, 201)
        self.assertEqual(Comment.objects.count(), 1)

    def test_create_course_validation_and_creation(self):
        self.client.force_authenticate(user=self.user)

        bad_resp = self.client.post('/api/v1/courses/create/', {'title': '   '}, format='json')
        self.assertEqual(bad_resp.status_code, 400)

        good_resp = self.client.post(
            '/api/v1/courses/create/',
            {
                'title': 'New Vue Course',
                'short_description': 'Short',
                'long_description': 'Long',
                'status': 'review',
                'categories': [self.category.id],
                'lessons': [{'title': 'Lesson 1', 'short_description': 'S1', 'long_description': 'L1'}],
            },
            format='json',
        )
        self.assertEqual(good_resp.status_code, 201)
        created = Course.objects.get(id=good_resp.data['course_id'])
        self.assertEqual(created.status, Course.IN_REVIEW)
        self.assertEqual(created.lessons.count(), 1)
