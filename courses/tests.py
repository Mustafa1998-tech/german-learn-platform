from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from .models import Level, Lesson, Exercise, Result

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.level = Level.objects.create(
            name='A1',
            description='Beginner Level'
        )
        self.lesson = Lesson.objects.create(
            title='Test Lesson',
            level=self.level,
            content='Test content',
            order=1
        )

    def test_home_view(self):
        response = self.client.get(reverse('courses:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertContains(response, 'Levels')

    def test_level_detail_view(self):
        response = self.client.get(
            reverse('courses:level_detail', args=[self.level.slug])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'level.html')
        self.assertContains(response, self.level.name)

    def test_lesson_detail_view(self):
        response = self.client.get(
            reverse('courses:lesson_detail', args=[self.lesson.slug])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lesson.html')
        self.assertContains(response, self.lesson.title)

    def test_lesson_detail_view_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(
            reverse('courses:lesson_detail', args=[self.lesson.slug])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lesson.html')

class TestModels(TestCase):
    def test_level_creation(self):
        level = Level.objects.create(
            name='A2',
            description='Elementary Level'
        )
        self.assertEqual(str(level), 'A2')
        self.assertEqual(level.slug, 'a2')
        self.assertEqual(level.description, 'Elementary Level')

    def test_lesson_creation(self):
        level = Level.objects.create(name='B1', description='Intermediate Level')
        lesson = Lesson.objects.create(
            title='Test Lesson',
            level=level,
            content='Test content',
            order=1
        )
        self.assertEqual(str(lesson), 'B1 - Test Lesson')
        self.assertTrue(lesson.slug.startswith('b1-'))
        self.assertEqual(lesson.level, level)
