# Dastavka API Documentation

Bu API suv va shunga o'xshash mahsulotlar dastavkasi uchun mobil ilova backend qismi.

## 📚 Interaktiv Dokumentatsiya

API uchun interaktiv dokumentatsiya mavjud:

- **Swagger UI**: [http://127.0.0.1:8000/api/docs/](http://127.0.0.1:8000/api/docs/)
- **ReDoc**: [http://127.0.0.1:8000/api/redoc/](http://127.0.0.1:8000/api/redoc/)
- **OpenAPI Schema**: [http://127.0.0.1:8000/api/schema/](http://127.0.0.1:8000/api/schema/)

## Base URL
```
http://127.0.0.1:8000/api/
```

## Users API Endpoints

### 1. User Registration (Ro'yxatdan o'tish)
**POST** `/api/users/register/`

**Request Body:**
```json
{
    "username": "test_user",
    "password": "secure_password123",
    "password_confirm": "secure_password123",
    "full_name": "Ism Familya",
    "role": "kuryer"
}
```

**Response:**
```json
{
    "message": "User muvaffaqiyatli ro'yxatdan o'tdi!",
    "user": {
        "id": 1,
        "username": "test_user",
        "full_name": "Ism Familya",
        "role": "kuryer",
        "status": "active",
        "created_at": "2025-11-08T13:59:00Z",
        "updated_at": "2025-11-08T13:59:00Z"
    },
    "token": "your_auth_token_here"
}
```

### 2. User Login (Kirish)
**POST** `/api/users/login/`

**Request Body:**
```json
{
    "username": "test_user",
    "password": "secure_password123"
}
```

**Response:**
```json
{
    "message": "Muvaffaqiyatli login!",
    "user": {
        "id": 1,
        "username": "test_user",
        "full_name": "Ism Familya",
        "role": "kuryer",
        "status": "active",
        "created_at": "2025-11-08T13:59:00Z",
        "updated_at": "2025-11-08T13:59:00Z"
    },
    "token": "your_auth_token_here"
}
```

### 3. User Profile (Profil ko'rish)
**GET** `/api/users/profile/`

**Headers:**
```
Authorization: Token your_auth_token_here
```

**Response:**
```json
{
    "id": 1,
    "username": "test_user",
    "full_name": "Ism Familya",
    "role": "kuryer",
    "status": "active",
    "created_at": "2025-11-08T13:59:00Z",
    "updated_at": "2025-11-08T13:59:00Z"
}
```

### 4. Update Profile (Profilni yangilash)
**PUT/PATCH** `/api/users/profile/update/`

**Headers:**
```
Authorization: Token your_auth_token_here
```

**Request Body:**
```json
{
    "full_name": "Yangi Ism Familya"
}
```

### 5. Users List (Barcha userlar - Admin uchun)
**GET** `/api/users/`

**Headers:**
```
Authorization: Token your_auth_token_here
```

### 6. User Detail (Bitta userning ma'lumotlari)
**GET** `/api/users/{id}/`

**Headers:**
```
Authorization: Token your_auth_token_here
```

### 7. User Logout (Chiqish)
**POST** `/api/users/logout/`

**Headers:**
```
Authorization: Token your_auth_token_here
```

**Response:**
```json
{
    "message": "Muvaffaqiyatli logout!"
}
```

## User Model Fields

- `id`: Auto-generated ID
- `username`: Login uchun unique username 
- `password`: Shifrlangan parol
- `full_name`: Ism-familya
- `role`: "admin" yoki "kuryer"
- `status`: "active" yoki "inactive"
- `created_at`: Yaratilgan sana
- `updated_at`: Yangilangan sana

## Authentication

API Token-based authentication ishlatadi. Har bir so'rov uchun header da token yuborish kerak:

```
Authorization: Token your_auth_token_here
```

Token login yoki registration paytida qaytariladi.

## Error Responses

API xatolik holatlarida quyidagicha javob qaytaradi:

```json
{
    "field_name": ["Error message here"],
    "non_field_errors": ["General error message"]
}
```

Status kodlar:
- 200: Muvaffaqiyatli
- 201: Yaratildi
- 400: Noto'g'ri so'rov
- 401: Autentifikatsiya kerak
- 403: Ruxsat yo'q
- 404: Topilmadi
- 500: Server xatosi