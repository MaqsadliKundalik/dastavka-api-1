# 🚚 Dastavka API

Suv va shunga o'xshash mahsulotlar dastavkasi uchun Django REST Framework asosida qurilgan API.

## 🚀 Xususiyatlar

- **Foydalanuvchi boshqaruvi**: Ro'yxatdan o'tish, kirish, profil boshqaruvi
- **Token-based Authentication**: Xavfsiz API kirish tizimi
- **Role-based Access**: Admin va Kuryer rollari
- **Interaktiv Dokumentatsiya**: Swagger UI va ReDoc
- **OpenAPI 3.0 Schema**: To'liq API spetsifikatsiyasi

## 📱 API Endpointlar

### 🔐 Authentication
- `POST /api/users/register/` - Ro'yxatdan o'tish
- `POST /api/users/login/` - Tizimga kirish
- `POST /api/users/logout/` - Tizimdan chiqish

### 👤 Profile
- `GET /api/users/profile/` - Profil ko'rish
- `PUT/PATCH /api/users/profile/update/` - Profilni yangilash

### 👥 Users (Admin uchun)
- `GET /api/users/` - Barcha foydalanuvchilar
- `POST /api/users/` - Yangi foydalanuvchi yaratish
- `GET /api/users/{id}/` - Bitta foydalanuvchi
- `PUT/PATCH /api/users/{id}/` - Foydalanuvchini yangilash
- `DELETE /api/users/{id}/` - Foydalanuvchini o'chirish

## 📚 Dokumentatsiya

**Interaktiv Dokumentatsiya:**
- [Swagger UI](http://127.0.0.1:8000/api/docs/) - API ni test qilish uchun
- [ReDoc](http://127.0.0.1:8000/api/redoc/) - Chiroyli dokumentatsiya
- [OpenAPI Schema](http://127.0.0.1:8000/api/schema/) - JSON/YAML schema

## 🛠 O'rnatish va ishga tushirish

### 1. Talablar
```bash
Python 3.8+
Django 5.2.8
Django REST Framework 3.16.1
drf-spectacular (dokumentatsiya uchun)
```

### 2. Virtual environment yaratish
```bash
python -m venv myenv
myenv\\Scripts\\activate  # Windows
source myenv/bin/activate  # Linux/Mac
```

### 3. Kerakli paketlarni o'rnatish
```bash
pip install django djangorestframework drf-spectacular
```

### 4. Database sozlash
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Superuser yaratish
```bash
python manage.py createsuperuser
```

### 6. Serverni ishga tushirish
```bash
python manage.py runserver
```

Server `http://127.0.0.1:8000/` da ishga tushadi.

## 📋 Foydalanuvchi Modeli

| Field | Type | Description |
|-------|------|-------------|
| `id` | Integer | Auto-generated ID |
| `username` | String | Login uchun unique username |
| `password` | String | Shifrlangan parol |
| `full_name` | String | To'liq ism-familya |
| `role` | Choice | "admin" yoki "kuryer" |
| `status` | Choice | "active" yoki "inactive" |
| `created_at` | DateTime | Yaratilgan sana |
| `updated_at` | DateTime | Yangilangan sana |

## 🔐 Authentication

API Token-based authentication ishlatadi. Header formatda token yuborish kerak:

```
Authorization: Token your_token_here
```

Token login yoki registration paytida qaytariladi.

## 🧪 API ni test qilish

### 1. Ro'yxatdan o'tish
```bash
POST /api/users/register/
{
    "username": "test_user",
    "password": "secure123456",
    "password_confirm": "secure123456",
    "full_name": "Test User",
    "role": "kuryer"
}
```

### 2. Login
```bash
POST /api/users/login/
{
    "username": "test_user",
    "password": "secure123456"
}
```

### 3. Profile ko'rish
```bash
GET /api/users/profile/
Headers: Authorization: Token your_token_here
```

## 🏗 Loyiha Tuzilmasi

```
dastavka-api/
├── dastavka/            # Django project settings
│   ├── settings.py      # Asosiy sozlamalar
│   ├── urls.py          # URL routing
│   └── wsgi.py          # WSGI konfiguratsiya
├── users/               # Users app
│   ├── models.py        # User modeli
│   ├── serializers.py   # DRF serializers
│   ├── views.py         # API views
│   ├── urls.py          # App URLs
│   └── admin.py         # Admin interface
├── manage.py            # Django management script
├── db.sqlite3           # SQLite database
└── requirements.txt     # Python dependencies
```

## 🔄 Keyingi Qadamlar

1. **Mahsulotlar API** - Suv va boshqa mahsulotlar uchun
2. **Buyurtmalar API** - Order management
3. **Manzillar API** - Delivery addresses
4. **Kuryer Tracking** - Real-time kuryer holati
5. **Push Notifications** - Mobile bildirishnomalar
6. **Payment Integration** - To'lov tizimini birlashtirish

## 🤝 Hissa qo'shish

1. Fork qiling
2. Feature branch yarating (`git checkout -b feature/yangi-xususiyat`)
3. O'zgarishlarni commit qiling (`git commit -am 'Yangi xususiyat qo'shildi'`)
4. Branch ga push qiling (`git push origin feature/yangi-xususiyat`)
5. Pull Request yarating

## 📄 License

Bu loyiha MIT License ostida chiqarilgan.

## 📞 Aloqa

Savollar yoki takliflar uchun murojaat qiling.

---

**Dastavka API** - Mobil ilova uchun ishonchli backend yechimi! 🚀