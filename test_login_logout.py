import os
import django
import requests

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dastavka.settings')
django.setup()

from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

# Create test user if not exists
User = get_user_model()
user, created = User.objects.get_or_create(
    username='testuser',
    defaults={
        'full_name': 'Test User',
        'role': 'admin'
    }
)
if created:
    user.set_password('testpass123')
    user.save()
    print("Test user created")
else:
    print("Test user already exists")

# Get or create token
token, created = Token.objects.get_or_create(user=user)
print(f"Token: {token.key}")

# Test login via API
base_url = 'http://127.0.0.1:8000/api'
login_data = {
    'username': 'testuser',
    'password': 'testpass123'
}

print("Testing login...")
try:
    response = requests.post(f'{base_url}/users/login/', json=login_data)
    print(f"Login status: {response.status_code}")
    print(f"Login response: {response.json()}")
except Exception as e:
    print(f"Login error: {e}")

# Test logout with token
print("Testing logout...")
try:
    headers = {'Authorization': f'Token {token.key}'}
    response = requests.post(f'{base_url}/users/logout/', headers=headers)
    print(f"Logout status: {response.status_code}")
    print(f"Logout response: {response.json()}")
except Exception as e:
    print(f"Logout error: {e}")