"""
API endpointlarini manual test qilish uchun
"""

# Quyidagi POST so'rovlarni manual ravishda amalga oshiring:

print("🚀 Dastavka API Test Ma'lumotlari")
print("=" * 50)

print("\n1️⃣ USER REGISTRATION:")
print("URL: http://127.0.0.1:8000/api/users/register/")
print("Method: POST")
print("Headers: Content-Type: application/json")
print("Body:")
registration_data = {
    "username": "test_kuryer",
    "password": "secure123456",
    "password_confirm": "secure123456",
    "full_name": "Jasur Karimov",
    "role": "kuryer"
}
import json
print(json.dumps(registration_data, indent=2, ensure_ascii=False))

print("\n2️⃣ USER LOGIN:")
print("URL: http://127.0.0.1:8000/api/users/login/")
print("Method: POST")
print("Headers: Content-Type: application/json")
print("Body:")
login_data = {
    "username": "test_kuryer",
    "password": "secure123456"
}
print(json.dumps(login_data, indent=2, ensure_ascii=False))

print("\n3️⃣ USER PROFILE:")
print("URL: http://127.0.0.1:8000/api/users/profile/")
print("Method: GET")
print("Headers: Authorization: Token YOUR_TOKEN_HERE")

print("\n4️⃣ USERS LIST:")
print("URL: http://127.0.0.1:8000/api/users/")
print("Method: GET")
print("Headers: Authorization: Token YOUR_TOKEN_HERE")

print("\n5️⃣ USER LOGOUT:")
print("URL: http://127.0.0.1:8000/api/users/logout/")
print("Method: POST")
print("Headers: Authorization: Token YOUR_TOKEN_HERE")

print("\n" + "=" * 50)
print("API Server: http://127.0.0.1:8000")
print("Admin Panel: http://127.0.0.1:8000/admin")
print("=" * 50)