from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from .models import Order


class OrdersAPITestCase(TestCase):
	def setUp(self):
		self.client = APIClient()
		User = get_user_model()
		# create admin (creator) and courier without using create_user
		self.creator = User(username='creator', full_name='Creator', role='admin')
		self.creator.set_password('pass123')
		self.creator.save()
		self.courier = User(username='courier', full_name='Courier', role='kuryer')
		self.courier.set_password('pass123')
		self.courier.save()

	def test_create_order_and_my_orders(self):
		# creator creates an order
		self.client.force_authenticate(user=self.creator)
		data = {
			'full_name': 'Client X',
			'phone_number': '+998901112233',
			'address': 'Test address 1',
			'direction': 'kiruvchi'
		}
		resp = self.client.post('/api/orders/', data, format='json')
		self.assertEqual(resp.status_code, 201)
		# OrderCreateSerializer does not return 'id' in POST response; fetch from DB
		order = Order.objects.filter(full_name='Client X').first()
		self.assertIsNotNone(order)
		order_id = order.id

		# as creator, /api/orders/my/ should return the order
		resp2 = self.client.get('/api/orders/my/')
		self.assertEqual(resp2.status_code, 200)
		self.assertTrue(any(o['id'] == order_id for o in resp2.data))

		# assign to courier and check courier's my orders
		order = Order.objects.get(pk=order_id)
		order.assigned_to = self.courier
		order.save()

		self.client.force_authenticate(user=self.courier)
		resp3 = self.client.get('/api/orders/my/')
		self.assertEqual(resp3.status_code, 200)
		self.assertTrue(any(o['id'] == order_id for o in resp3.data))
