from django.contrib.auth.models import User
from django.test import TestCase

from apps.models import TextCustomQuestion, QuestionCategory, GameMode, ImageCustomQuestion
from apps.question import generate_question, FailedToGenerateQuestion
from apps.utils import create_all_weighted


class BaseTestCase(TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
        )
        self.user.is_staff = True
        self.user.save()

    def login(self):
        self.client.login(username=self.username, password=self.password)

    def logout(self):
        self.client.logout()

    def set_as_superuser(self):
        self.user.is_superuser = True
        self.user.save()


class TestQuestionGenerator(TestCase):
    def test_generate_question_custom_text_question(self):
        question_category = QuestionCategory.objects.create(name="Dummy category")
        for i in range(5):
            TextCustomQuestion.objects.create(
                question="Dummy question",
                choices=f'["{i}","{i+1}","{i+2}","{i+3}"]',
                answer=f'["{i}"]',
                difficulty_level="easy",
                category=question_category,
                active=True
            )
        GameMode.objects.create(name="Dummy mode", allow_answer_mode="single_right")
        for i in range(5):
            response = self.client.get('/api/random_question')
            self.assertEqual(response.status_code, 200)

    def test_generate_question_custom_text_question_not_enough_choice(self):
        question_category = QuestionCategory.objects.create(name="Dummy category")
        for i in range(5):
            TextCustomQuestion.objects.create(
                question="Dummy question",
                choices=f'["{i}","{i + 1}"]',
                answer=f'["{i}"]',
                difficulty_level="easy",
                category=question_category,
                active=True
            )
        GameMode.objects.create(name="Dummy mode", allow_answer_mode="single_right")
        for i in range(5):
            response = self.client.get('/api/random_question')
            self.assertEqual(response.status_code, 400)

    def test_generate_question_custom_image(self):
        question_category = QuestionCategory.objects.create(name="Dummy category")
        for i in range(5):
            ImageCustomQuestion.objects.create(
                question="Dummy question",
                choices=f'["{i}","{i + 1}","{i + 2}","{i + 3}"]',
                answer=f'["{i}"]',
                difficulty_level="easy",
                category=question_category,
                active=True
            )
        GameMode.objects.create(name="Dummy mode", allow_answer_mode="single_right")
        for i in range(5):
            response = self.client.get('/api/random_question')
            self.assertEqual(response.status_code, 200)

    def test_generate_question_custom_image_not_enough_choice(self):
        question_category = QuestionCategory.objects.create(name="Dummy category")
        for i in range(5):
            ImageCustomQuestion.objects.create(
                question="Dummy question",
                choices=f'["{i}","{i + 1}"]',
                answer=f'["{i}"]',
                difficulty_level="easy",
                category=question_category,
                active=True
            )
        GameMode.objects.create(name="Dummy mode", allow_answer_mode="single_right")
        for i in range(5):
            response = self.client.get('/api/random_question')
            self.assertEqual(response.status_code, 400)

    def test_generate_question_fail_attempts(self):
        # No category
        self.assertRaises(FailedToGenerateQuestion, generate_question)


class TestQuestionGeneratorWithUser(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.login()

    def test_generate_question_custom_text_question(self):
        question_category = QuestionCategory.objects.create(name="Dummy category")
        create_all_weighted()
        for i in range(5):
            TextCustomQuestion.objects.create(
                question="Dummy question",
                choices=f'["{i}","{i+1}","{i+2}","{i+3}"]',
                answer=f'["{i}"]',
                difficulty_level="easy",
                category=question_category,
                active=True
            )
        GameMode.objects.create(name="Dummy mode", allow_answer_mode="single_right")
        for i in range(5):
            response = self.client.get('/api/random_question')
            self.assertEqual(response.status_code, 200)

    def test_generate_question_custom_text_question_not_enough_choice(self):
        question_category = QuestionCategory.objects.create(name="Dummy category")
        create_all_weighted()
        for i in range(5):
            TextCustomQuestion.objects.create(
                question="Dummy question",
                choices=f'["{i}","{i + 1}"]',
                answer=f'["{i}"]',
                difficulty_level="easy",
                category=question_category,
                active=True
            )
        GameMode.objects.create(name="Dummy mode", allow_answer_mode="single_right")
        for i in range(5):
            response = self.client.get('/api/random_question')
            self.assertEqual(response.status_code, 400)

    def test_generate_question_custom_image(self):
        question_category = QuestionCategory.objects.create(name="Dummy category")
        create_all_weighted()
        for i in range(5):
            ImageCustomQuestion.objects.create(
                question="Dummy question",
                choices=f'["{i}","{i + 1}","{i + 2}","{i + 3}"]',
                answer=f'["{i}"]',
                difficulty_level="easy",
                category=question_category,
                active=True
            )
        GameMode.objects.create(name="Dummy mode", allow_answer_mode="single_right")
        for i in range(5):
            response = self.client.get('/api/random_question')
            self.assertEqual(response.status_code, 200)

    def test_generate_question_custom_image_not_enough_choice(self):
        question_category = QuestionCategory.objects.create(name="Dummy category")
        create_all_weighted()
        for i in range(5):
            ImageCustomQuestion.objects.create(
                question="Dummy question",
                choices=f'["{i}","{i + 1}"]',
                answer=f'["{i}"]',
                difficulty_level="easy",
                category=question_category,
                active=True
            )
        GameMode.objects.create(name="Dummy mode", allow_answer_mode="single_right")
        for i in range(5):
            response = self.client.get('/api/random_question')
            self.assertEqual(response.status_code, 400)