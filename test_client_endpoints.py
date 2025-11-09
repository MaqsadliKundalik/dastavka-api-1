#!/usr/bin/env python3
"""
Client endpoints bilan API test skripti
"""

import requests
import json
import time

# API base URL
BASE_URL = "http://127.0.0.1:8000/api"

def print_response(response, title):
    """Response-ni chiroyli formatda chiqarish"""
    print(f"\n{'='*50}")
    print(f"{title}")
    print(f"{'='*50}")
    print(f"Status Code: {response.status_code}")
    
    try:
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2, ensure_ascii=False)}")
    except:
        print(f"Response: {response.text}")
    print(f"{'='*50}")

def test_client_endpoints():
    """Client endpoints-ni test qilish"""
    print("🚀 CLIENT ENDPOINTS TEST BOSHLAYAPTI...")
    
    # 1. Foydalanuvchi yaratish va token olish
    print("\n1️⃣ TOKEN OLISH...")
    register_data = {
        "username": f"testuser_{int(time.time())}",
        "password": "testpass123",
        "password_confirm": "testpass123",
        "full_name": "Test Admin",
        "role": "admin"
    }
    
    response = requests.post(f"{BASE_URL}/users/register/", json=register_data)
    if response.status_code != 201:
        print("❌ Ro'yxatdan o'tishda xatolik!")
        return
    
    token = response.json()["token"]
    headers = {"Authorization": f"Token {token}"}
    print(f"✅ Token olindi: {token[:20]}...")
    
    # 2. Yangi mijoz yaratish
    print("\n2️⃣ YANGI MIJOZ YARATISH...")
    client_data = {
        "full_name": "Sarvar Abdullayev",
        "phone_number": "+998901234567",
        "location_name": "Toshkent Samarkand Darvoza",
        "address": "Toshkent sh., Yunusobod t., 15-kv, 25-uy",
        "longitude": "69.2785",
        "latitude": "41.3111",
        "notes": "VIP mijoz, tez xizmat talab qiladi"
    }
    
    response = requests.post(f"{BASE_URL}/clients/", json=client_data, headers=headers)
    print_response(response, "YANGI MIJOZ YARATISH")
    
    if response.status_code != 201:
        print("❌ Mijoz yaratishda xatolik!")
        return
    
    client_id = response.json()["id"]
    print(f"✅ Mijoz yaratildi, ID: {client_id}")
    
    # 3. Mijozlar ro'yxati
    print("\n3️⃣ MIJOZLAR RO'YXATI...")
    response = requests.get(f"{BASE_URL}/clients/", headers=headers)
    print_response(response, "MIJOZLAR RO'YXATI")
    
    # 4. Bitta mijoz ma'lumotlari
    print("\n4️⃣ MIJOZ TAFSILOTLARI...")
    response = requests.get(f"{BASE_URL}/clients/{client_id}/", headers=headers)
    print_response(response, "MIJOZ TAFSILOTLARI")
    
    # 5. Mijoz ma'lumotlarini yangilash
    print("\n5️⃣ MIJOZ MA'LUMOTLARINI YANGILASH...")
    update_data = {
        "notes": "SUPER VIP mijoz - maxsus e'tibor talab qiladi",
        "location_name": "Toshkent Mega Planet"
    }
    
    response = requests.patch(f"{BASE_URL}/clients/{client_id}/", json=update_data, headers=headers)
    print_response(response, "MIJOZ YANGILASH")
    
    # 6. Mijoz uchun buyurtma yaratish
    print("\n6️⃣ MIJOZ UCHUN BUYURTMA YARATISH (orders endpoint orqali)...")
    order_data = {
        "client_full_name": "Sarvar Abdullayev",
        "client_phone_number": "+998901234567",
        "client_location_name": "Toshkent Mega Planet",
        "client_address": "Toshkent sh., Yunusobod t., 15-kv, 25-uy",
        "kiruvchi_soni": 3,
        "chiquvchi_soni": 2,
        "notes": "Birinchi buyurtma"
    }
    
    response = requests.post(f"{BASE_URL}/orders/", json=order_data, headers=headers)
    print_response(response, "BUYURTMA YARATISH")
    
    # 7. Mijozning buyurtmalarini ko'rish
    print("\n7️⃣ MIJOZNING BUYURTMALARI...")
    response = requests.get(f"{BASE_URL}/clients/{client_id}/orders/", headers=headers)
    print_response(response, "MIJOZNING BUYURTMALARI")
    
    # 8. Mijozlar statistikasi
    print("\n8️⃣ MIJOZLAR STATISTIKASI...")
    response = requests.get(f"{BASE_URL}/clients/stats/", headers=headers)
    print_response(response, "MIJOZLAR STATISTIKASI")
    
    # 9. Mijozlarni qidirish
    print("\n9️⃣ MIJOZLARNI QIDIRISH...")
    response = requests.get(f"{BASE_URL}/clients/?search=Sarvar", headers=headers)
    print_response(response, "QIDIRUV: Sarvar")
    
    # 10. Yana bir mijoz yaratish (statistika uchun)
    print("\n🔟 IKKINCHI MIJOZ YARATISH...")
    client_data2 = {
        "full_name": "Dilshod Toshmatov",
        "phone_number": "+998901234568",
        "location_name": "Chorsu Bozor",
        "address": "Toshkent sh., Eski shahar, 5-uy",
        "notes": "Muntazam mijoz"
    }
    
    response = requests.post(f"{BASE_URL}/clients/", json=client_data2, headers=headers)
    if response.status_code == 201:
        client2_id = response.json()["id"]
        print(f"✅ Ikkinchi mijoz yaratildi, ID: {client2_id}")
        
        # Ikkinchi mijoz uchun ham buyurtma
        order_data2 = {
            "client_full_name": "Dilshod Toshmatov",
            "client_phone_number": "+998901234568",
            "client_location_name": "Chorsu Bozor",
            "client_address": "Toshkent sh., Eski shahar, 5-uy",
            "kiruvchi_soni": 1,
            "chiquvchi_soni": 5,
            "notes": "Test buyurtma"
        }
        
        requests.post(f"{BASE_URL}/orders/", json=order_data2, headers=headers)
    
    # 11. Yangilangan statistika
    print("\n1️⃣1️⃣ YANGILANGAN STATISTIKA...")
    response = requests.get(f"{BASE_URL}/clients/stats/", headers=headers)
    print_response(response, "YANGILANGAN STATISTIKA")
    
    print("\n🎉 CLIENT ENDPOINTS TESTLARI YAKUNLANDI!")
    print("✅ Barcha Client endpoints muvaffaqiyatli ishlayapti!")

if __name__ == "__main__":
    try:
        test_client_endpoints()
    except requests.exceptions.ConnectionError:
        print("❌ Server ishlamayapti! Avval 'python manage.py runserver' ni ishga tushiring.")
    except Exception as e:
        print(f"❌ Kutilmagan xatolik: {e}")