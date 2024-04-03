from django.contrib.auth.models import User
from django.test import TestCase


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
