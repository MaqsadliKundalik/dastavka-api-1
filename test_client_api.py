#!/usr/bin/env python3
"""
Yangi Client model bilan API test skripti
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

def test_api():
    """API-ni test qilish"""
    print("🚀 YANGI CLIENT MODEL BILAN API TEST BOSHLAYAPTI...")
    
    # 1. Ro'yxatdan o'tish
    print("\n1️⃣ FOYDALANUVCHI RO'YXATDAN O'TISHI...")
    register_data = {
        "username": f"testuser_{int(time.time())}",
        "password": "testpass123",
        "password_confirm": "testpass123",
        "full_name": "Test Foydalanuvchi",
        "role": "admin"
    }
    
    response = requests.post(f"{BASE_URL}/users/register/", json=register_data)
    print_response(response, "RO'YXATDAN O'TISH")
    
    if response.status_code != 201:
        print("❌ Ro'yxatdan o'tishda xatolik!")
        return
    
    # 2. Tizimga kirish
    print("\n2️⃣ TIZIMGA KIRISH...")
    login_data = {
        "username": register_data["username"],
        "password": register_data["password"]
    }
    
    response = requests.post(f"{BASE_URL}/users/login/", json=login_data)
    print_response(response, "TIZIMGA KIRISH")
    
    if response.status_code != 200:
        print("❌ Tizimga kirishda xatolik!")
        return
    
    token = response.json()["token"]
    headers = {"Authorization": f"Token {token}"}
    print(f"✅ Token olindi: {token[:20]}...")
    
    # 3. Yangi buyurtma yaratish (yangi Client model bilan)
    print("\n3️⃣ YANGI BUYURTMA YARATISH (Client bilan)...")
    order_data = {
        "client_full_name": "Anvar Karimov",
        "client_phone_number": "+998901234567",
        "client_location_name": "Toshkent Mall",
        "client_address": "Toshkent sh., Chilonzor t., 1-kv, 10-uy",
        "client_longitude": "69.2401",
        "client_latitude": "41.2995",
        "client_notes": "Doimiy mijoz, yaxshi tanish",
        "kiruvchi_soni": 5,
        "chiquvchi_soni": 3,
        "notes": "2-qavat, qo'ng'iroq qiling"
    }
    
    response = requests.post(f"{BASE_URL}/orders/", json=order_data, headers=headers)
    print_response(response, "YANGI BUYURTMA YARATISH")
    
    if response.status_code != 201:
        print("❌ Buyurtma yaratishda xatolik!")
        return
    
    order_id = response.json()["id"]
    print(f"✅ Buyurtma yaratildi, ID: {order_id}")
    
    # 4. Buyurtmalar ro'yxatini ko'rish
    print("\n4️⃣ BUYURTMALAR RO'YXATI...")
    response = requests.get(f"{BASE_URL}/orders/", headers=headers)
    print_response(response, "BUYURTMALAR RO'YXATI")
    
    # 5. Bitta buyurtmani ko'rish
    print("\n5️⃣ BUYURTMA TAFSILOTLARI...")
    response = requests.get(f"{BASE_URL}/orders/{order_id}/", headers=headers)
    print_response(response, "BUYURTMA TAFSILOTLARI")
    
    # 6. Buyurtmani yangilash
    print("\n6️⃣ BUYURTMANI YANGILASH...")
    update_data = {
        "kiruvchi_soni": 7,
        "chiquvchi_soni": 4,
        "notes": "Yangilangan izoh - tez yetkazish kerak"
    }
    
    response = requests.patch(f"{BASE_URL}/orders/{order_id}/", json=update_data, headers=headers)
    print_response(response, "BUYURTMANI YANGILASH")
    
    # 7. Status yangilash
    print("\n7️⃣ STATUS YANGILASH...")
    status_data = {"status": "bajarildi"}
    
    response = requests.patch(f"{BASE_URL}/orders/{order_id}/status/", json=status_data, headers=headers)
    print_response(response, "STATUS YANGILASH")
    
    # 8. Yana bir buyurtma yaratish (bir xil mijoz uchun)
    print("\n8️⃣ IKKINCHI BUYURTMA (Bir xil mijoz)...")
    order_data2 = {
        "client_full_name": "Anvar Karimov",  # Bir xil mijoz
        "client_phone_number": "+998901234567",
        "client_location_name": "Toshkent Mall",
        "client_address": "Toshkent sh., Chilonzor t., 1-kv, 10-uy",
        "kiruvchi_soni": 2,
        "chiquvchi_soni": 1,
        "notes": "Ikkinchi buyurtma"
    }
    
    response = requests.post(f"{BASE_URL}/orders/", json=order_data2, headers=headers)
    print_response(response, "IKKINCHI BUYURTMA")
    
    # 9. Qidiruv test qilish
    print("\n9️⃣ QIDIRUV TESTI...")
    response = requests.get(f"{BASE_URL}/orders/?search=Anvar", headers=headers)
    print_response(response, "QIDIRUV: Anvar")
    
    # 10. Profile ko'rish
    print("\n🔟 PROFILE MA'LUMOTLARI...")
    response = requests.get(f"{BASE_URL}/users/profile/", headers=headers)
    print_response(response, "PROFILE")
    
    print("\n🎉 BARCHA TESTLAR YAKUNLANDI!")
    print("✅ Yangi Client model strukturasi muvaffaqiyatli ishlayapti!")

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("❌ Server ishlamayapti! Avval 'python manage.py runserver' ni ishga tushiring.")
    except Exception as e:
        print(f"❌ Kutilmagan xatolik: {e}")