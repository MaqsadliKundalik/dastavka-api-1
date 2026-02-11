from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token


class UsersAPITestCase(TestCase):
	def setUp(self):
		self.client = APIClient()
		User = get_user_model()
		self.user = User(username='test_user', full_name='Test User', role='admin')
		self.user.set_password('pass12345')
		self.user.save()

	def test_profile_requires_auth(self):
		resp = self.client.get('/api/users/profile/')
		self.assertEqual(resp.status_code, 401)

	def test_profile_retrieval_and_update(self):
		self.client.force_authenticate(user=self.user)
		resp = self.client.get('/api/users/profile/')
		self.assertEqual(resp.status_code, 200)
		self.assertIn('username', resp.data)

		resp2 = self.client.put('/api/users/profile/', {'full_name': 'Updated Name'}, format='json')
		self.assertEqual(resp2.status_code, 200)
		self.user.refresh_from_db()
		self.assertEqual(self.user.full_name, 'Updated Name')

	def test_user_login_success(self):
		data = {
			'username': 'test_user',
			'password': 'pass12345'
		}
		resp = self.client.post('/api/users/login/', data, format='json')
		self.assertEqual(resp.status_code, 200)
		self.assertIn('token', resp.data)
		self.assertIn('user', resp.data)
		self.assertEqual(resp.data['user']['username'], 'test_user')

		token_exists = Token.objects.filter(user=self.user).exists()
		self.assertTrue(token_exists)

	def test_user_login_wrong_credentials(self):
		data = {
			'username': 'test_user',
			'password': 'wrongpass'
		}
		resp = self.client.post('/api/users/login/', data, format='json')
		self.assertEqual(resp.status_code, 400)
		self.assertIn('non_field_errors', resp.data)

	def test_user_logout_success(self):
		data = {
			'username': 'test_user',
			'password': 'pass12345'
		}
		resp = self.client.post('/api/users/login/', data, format='json')
		token = resp.data['token']
		
		self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
		
		resp2 = self.client.post('/api/users/logout/')
		self.assertEqual(resp2.status_code, 200)
		self.assertIn('success', resp2.data)
		self.assertTrue(resp2.data['success'])

		token_exists = Token.objects.filter(user=self.user).exists()
		self.assertFalse(token_exists)

	def test_user_logout_unauthenticated(self):
		resp = self.client.post('/api/users/logout/')
		self.assertEqual(resp.status_code, 200)
		self.assertIn('success', resp.data)
		self.assertTrue(resp.data['success'])
