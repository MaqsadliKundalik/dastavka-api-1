from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient


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
		resp2 = self.client.put('/api/users/profile/update/', {'full_name': 'Updated Name'}, format='json')
		self.assertEqual(resp2.status_code, 200)
		self.user.refresh_from_db()
		self.assertEqual(self.user.full_name, 'Updated Name')
