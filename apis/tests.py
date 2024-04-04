from django.contrib.auth.models import User
from django.test import TestCase, Client

from apps.models import Game, QuestionCategory, ImageCustomQuestion, GameMode, TextCustomQuestion, GameQuestion


class TestObtainAuthToken(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

    def test_obtain_auth_token(self):
        response = self.client.post('/api/token', {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertIn('access', response_json)
        self.assertIn('refresh', response_json)
        self.header = {'HTTP_AUTHORIZATION': f'Bearer {response_json["access"]}'}
        response = self.client.post('/api/token/verify', {'token': response_json['access']})
        self.assertEqual(response.status_code, 200)

    def test_refresh_auth_token(self):
        response = self.client.post('/api/token', {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.header = {'HTTP_AUTHORIZATION': f'Bearer {response_json["access"]}'}
        response = self.client.post('/api/token/refresh', {'refresh': response_json['refresh']})
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertIn('access', response_json)
        self.assertNotIn('refresh', response_json)
        response = self.client.post('/api/token/verify', {'token': response_json['access']})
        self.assertEqual(response.status_code, 200)


class BaseAPITestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        response = self.client.post('/api/token', {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.header = {'HTTP_AUTHORIZATION': f'Bearer {response_json["access"]}'}
        self.client = Client(
            HTTP_AUTHORIZATION=f'Bearer {response_json["access"]}'
        )

    def generate_dummy_question(self):
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
            TextCustomQuestion.objects.create(
                question="Dummy question",
                choices=f'["{i}","{i + 1}","{i + 2}","{i + 3}"]',
                answer=f'["{i}"]',
                difficulty_level="easy",
                category=question_category,
                active=True
            )
        GameMode.objects.create(name="Dummy mode", allow_answer_mode="single_right")


class TestStartNewGame(BaseAPITestCase):
    def test_start_new_game(self):
        response = self.client.post('/api/game/start')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Game.objects.count(), 1)
        game = Game.objects.first()
        self.assertEqual(game.completed, False)
        self.assertEqual(game.finished, False)

    def test_start_new_game_without_auth(self):
        self.client = Client()
        response = self.client.post('/api/game/start')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(Game.objects.count(), 0)

    def test_start_new_game_have_unfinished_game(self):
        Game.objects.create(user=self.user, completed=False, finished=False)
        response = self.client.post('/api/game/start')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Game.objects.count(), 2)
        self.assertEqual(Game.objects.filter(completed=False, finished=False).count(), 1)
        self.assertEqual(Game.objects.filter(completed=False, finished=True).count(), 1)


class TestGenerateQuestionInGame(BaseAPITestCase):
    def test_generate_question_in_game(self):
        self.generate_dummy_question()
        game = Game.objects.create(user=self.user, completed=False, finished=False)
        response = self.client.post('/api/game/question', **self.header)
        self.assertEqual(response.status_code, 200)
        game.refresh_from_db()
        self.assertEqual(game.gamequestion_set.count(), 1)

    def test_generate_question_in_game_without_auth(self):
        self.generate_dummy_question()
        self.client = Client()
        game = Game.objects.create(user=self.user, completed=False, finished=False)
        response = self.client.post('/api/game/question')
        self.assertEqual(response.status_code, 401)
        game.refresh_from_db()
        self.assertEqual(game.gamequestion_set.count(), 0)

    def test_generate_question_in_game_no_running_game(self):
        self.generate_dummy_question()
        response = self.client.post('/api/game/question', **self.header)
        self.assertEqual(response.status_code, 400)

    def test_generate_question_in_game_have_unanswered_question(self):
        self.generate_dummy_question()
        game = Game.objects.create(user=self.user, completed=False, finished=False)
        response = self.client.post('/api/game/question', **self.header)
        self.assertEqual(response.status_code, 200)
        response = self.client.post('/api/game/question', **self.header)
        self.assertEqual(response.status_code, 400)
        game.refresh_from_db()
        self.assertEqual(game.gamequestion_set.count(), 1)

    def test_generate_question_in_game_failed_to_generate(self):
        game = Game.objects.create(user=self.user, completed=False, finished=False)
        response = self.client.post('/api/game/question', **self.header)
        self.assertEqual(response.status_code, 400)
        game.refresh_from_db()
        self.assertEqual(game.gamequestion_set.count(), 0)


class TestAnswerQuestion(BaseAPITestCase):
    def test_answer_question(self):
        self.generate_dummy_question()
        game = Game.objects.create(user=self.user, completed=False, finished=False)
        response = self.client.post('/api/game/question', **self.header)
        self.assertEqual(response.status_code, 200)
        game.refresh_from_db()
        question = game.gamequestion_set.first()
        response = self.client.post('/api/game/answer', {'answer': question.question.answer, 'duration': 5}, **self.header)
        self.assertEqual(response.status_code, 200)
        game_question = GameQuestion.objects.first()
        self.assertEqual(game_question.answered, True)
        self.assertEqual(game_question.selected, question.question.answer)
        self.assertEqual(game_question.is_true, True)

    def test_answer_question_wrong_answer(self):
        self.generate_dummy_question()
        game = Game.objects.create(user=self.user, completed=False, finished=False)
        response = self.client.post('/api/game/question', **self.header)
        self.assertEqual(response.status_code, 200)
        game.refresh_from_db()
        question = game.gamequestion_set.first()
        response = self.client.post('/api/game/answer', {'answer': '', 'duration': 5}, **self.header)
        self.assertEqual(response.status_code, 200)
        game_question = GameQuestion.objects.first()
        self.assertEqual(game_question.answered, True)
        self.assertEqual(game_question.selected, '')
        self.assertEqual(game_question.is_true, False)

    def test_answer_question_invalid_payload(self):
        self.generate_dummy_question()
        game = Game.objects.create(user=self.user, completed=False, finished=False)
        response = self.client.post('/api/game/question', **self.header)
        self.assertEqual(response.status_code, 200)
        game.refresh_from_db()
        question = game.gamequestion_set.first()
        response = self.client.post('/api/game/answer', {'duration': 5}, **self.header)
        self.assertEqual(response.status_code, 400)
        game_question = GameQuestion.objects.first()
        self.assertEqual(game_question.answered, False)
        self.assertEqual(game_question.is_true, False)

    def test_answer_question_without_auth(self):
        self.generate_dummy_question()
        self.client = Client()
        game = Game.objects.create(user=self.user, completed=False, finished=False)
        response = self.client.post('/api/game/question')
        self.assertEqual(response.status_code, 401)
        game.refresh_from_db()
        self.assertEqual(game.gamequestion_set.count(), 0)

    def test_answer_question_check_lost(self):
        self.generate_dummy_question()
        game = Game.objects.create(user=self.user, completed=False, finished=False)
        for i in range(3):
            response = self.client.post('/api/game/question', **self.header)
            self.assertEqual(response.status_code, 200)
            game.refresh_from_db()
            game.gamequestion_set.first()
            response = self.client.post('/api/game/answer', {'answer': '', 'duration': 5}, **self.header)
            self.assertEqual(response.status_code, 200)
            game_question = GameQuestion.objects.first()
            self.assertEqual(game_question.answered, True)
            self.assertEqual(game_question.selected, '')
            self.assertEqual(game_question.is_true, False)
        game.refresh_from_db()
        self.assertEqual(game.has_lose(), True)

    def test_answer_question_no_running_game(self):
        self.generate_dummy_question()
        response = self.client.post('/api/game/answer', {'answer': '["0"]', 'duration': 5}, **self.header)
        self.assertEqual(response.status_code, 400)

    def test_answer_question_no_question(self):
        self.generate_dummy_question()
        Game.objects.create(user=self.user, completed=False, finished=False)
        response = self.client.post('/api/game/answer', {'answer': '["0"]', 'duration': 5}, **self.header)
        self.assertEqual(response.status_code, 400)


class TestEndGame(BaseAPITestCase):
    def test_end_game(self):
        game = Game.objects.create(user=self.user, completed=False, finished=False)
        response = self.client.post('/api/game/end')
        self.assertEqual(response.status_code, 200)
        game.refresh_from_db()
        self.assertEqual(game.completed, True)
        self.assertEqual(game.finished, True)

    def test_answer_question_have_answered_question(self):
        self.generate_dummy_question()
        game = Game.objects.create(user=self.user, completed=False, finished=False)
        response = self.client.post('/api/game/question', **self.header)
        self.assertEqual(response.status_code, 200)
        game.refresh_from_db()
        question = game.gamequestion_set.first()
        response = self.client.post('/api/game/answer', {'answer': question.question.answer, 'duration': 5}, **self.header)
        self.assertEqual(response.status_code, 200)
        game.refresh_from_db()
        response = self.client.post('/api/game/end', **self.header)
        self.assertEqual(response.status_code, 200)
        game.refresh_from_db()
        self.assertEqual(game.completed, True)
        self.assertEqual(game.finished, True)

    def test_end_game_without_auth(self):
        self.client = Client()
        game = Game.objects.create(user=self.user, completed=False, finished=False)
        response = self.client.post('/api/game/end')
        self.assertEqual(response.status_code, 401)
        game.refresh_from_db()
        self.assertEqual(game.completed, False)
        self.assertEqual(game.finished, False)

    def test_end_game_no_running_game(self):
        response = self.client.post('/api/game/end')
        self.assertEqual(response.status_code, 400)


class TestGetUserInfo(BaseAPITestCase):
    def test_get_user_info(self):
        response = self.client.get('/api/user', **self.header)
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertIn('username', response_json)

    def test_get_user_info_without_auth(self):
        self.client = Client()
        response = self.client.get('/api/user')
        self.assertEqual(response.status_code, 401)


class TestGetLeaderboard(BaseAPITestCase):
    def test_get_leaderboard(self):
        response = self.client.get('/api/leaderboard', **self.header)
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertIsInstance(response_json, dict)


class TestGetPlayHistory(BaseAPITestCase):
    def test_get_play_history(self):
        game = Game.objects.create(user=self.user, completed=True, finished=True)
        response = self.client.get(f'/api/history/{game.id}', **self.header)
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertEqual(response_json['score'], game.score)

    def test_get_play_history_invalid_game_id(self):
        response = self.client.get(f'/api/history/0', **self.header)
        self.assertEqual(response.status_code, 404)
