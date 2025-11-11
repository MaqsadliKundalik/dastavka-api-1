from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token


class UsersAPITestCase(TestCase):
	def setUp(self):
		self.client = APIClient()
		User = get_user_model()
		# create a regular user without using create_user (custom model has no email)
		self.user = User(username='test_user', full_name='Test User', role='admin')
		self.user.set_password('pass12345')
		self.user.save()

	def test_profile_requires_auth(self):
		# unauthenticated should be rejected
		resp = self.client.get('/api/users/profile/')
		self.assertEqual(resp.status_code, 401)

	def test_profile_retrieval_and_update(self):
		# authenticate
		self.client.force_authenticate(user=self.user)
		resp = self.client.get('/api/users/profile/')
		self.assertEqual(resp.status_code, 200)
		self.assertIn('username', resp.data)

		# update full_name
		resp2 = self.client.put('/api/users/profile/', {'full_name': 'Updated Name'}, format='json')
		self.assertEqual(resp2.status_code, 200)
		self.user.refresh_from_db()
		self.assertEqual(self.user.full_name, 'Updated Name')

	def test_user_login_success(self):
		# successful login
		data = {
			'username': 'test_user',
			'password': 'pass12345'
		}
		resp = self.client.post('/api/users/login/', data, format='json')
		self.assertEqual(resp.status_code, 200)
		self.assertIn('token', resp.data)
		self.assertIn('user', resp.data)
		self.assertEqual(resp.data['user']['username'], 'test_user')

		# verify token was created
		token_exists = Token.objects.filter(user=self.user).exists()
		self.assertTrue(token_exists)

	def test_user_login_wrong_credentials(self):
		# wrong password
		data = {
			'username': 'test_user',
			'password': 'wrongpass'
		}
		resp = self.client.post('/api/users/login/', data, format='json')
		self.assertEqual(resp.status_code, 400)
		self.assertIn('non_field_errors', resp.data)

	def test_user_logout_success(self):
		# first login to get token
		data = {
			'username': 'test_user',
			'password': 'pass12345'
		}
		resp = self.client.post('/api/users/login/', data, format='json')
		token = resp.data['token']
		
		# authenticate with token
		self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
		
		# logout
		resp2 = self.client.post('/api/users/logout/')
		self.assertEqual(resp2.status_code, 200)
		self.assertIn('message', resp2.data)

		# verify token was deleted
		token_exists = Token.objects.filter(user=self.user).exists()
		self.assertFalse(token_exists)

	def test_user_logout_unauthenticated(self):
		# logout without authentication should still succeed
		resp = self.client.post('/api/users/logout/')
		self.assertEqual(resp.status_code, 200)
		self.assertIn('message', resp.data)
