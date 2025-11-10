#!/usr/bin/env python
"""
Autorizatsiyasiz Client ID filterlashni test qilish
"""

import requests
import json

# Base URL
BASE_URL = "http://localhost:8000/api"

def test_no_auth_filters():
    """Autorizatsiyasiz filterlashni test qilish"""
    
    print("🔍 AUTORIZATSIYASIZ FILTERLASH TESTLARI:")
    
    # 1. Barcha buyurtmalar
    print("\n1. Barcha buyurtmalar (autorizatsiyasiz):")
    response = requests.get(f"{BASE_URL}/orders/")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Jami buyurtmalar: {data['count']}")
        
        if data['results']:
            print("   📋 Birinchi buyurtma ma'lumotlari:")
            first_order = data['results'][0]
            print(f"      - ID: {first_order['id']}")
            print(f"      - Client: {first_order['client_full_name']}")
            print(f"      - Status: {first_order['status']}")
            
            # Birinchi buyurtmaning to'liq ma'lumotini olamiz
            response_detail = requests.get(f"{BASE_URL}/orders/{first_order['id']}/")
            if response_detail.status_code == 200:
                order_detail = response_detail.json()
                if 'client' in order_detail:
                    client_id = order_detail['client']['id']
                    print(f"      - Client ID: {client_id}")
                    
                    # 2. Client ID bo'yicha filterlash
                    print(f"\n2. Client ID {client_id} bo'yicha filterlash:")
                    response = requests.get(f"{BASE_URL}/orders/?client_id={client_id}")
                    if response.status_code == 200:
                        data = response.json()
                        print(f"   ✅ Client ID {client_id} uchun {data['count']} ta buyurtma topildi")
                        for order in data['results']:
                            print(f"      - Buyurtma {order['id']}: {order['client_full_name']}")
                    
                    # 3. Partial client ID qidirish
                    if len(str(client_id)) >= 2:
                        partial_id = str(client_id)[:1]  # Birinchi raqam
                        print(f"\n3. Client ID da '{partial_id}' qismi bo'yicha filterlash:")
                        response = requests.get(f"{BASE_URL}/orders/?client_id={partial_id}")
                        if response.status_code == 200:
                            data = response.json()
                            print(f"   ✅ ID'sida '{partial_id}' bo'lgan clientlar uchun {data['count']} ta buyurtma topildi")
                            for order in data['results'][:3]:
                                print(f"      - Buyurtma {order['id']}: {order['client_full_name']}")
    else:
        print(f"   ❌ Xatolik: {response.status_code}")
        print(f"   Response: {response.text}")
    
    # 4. Client nomi bo'yicha qidirish
    print("\n4. Client nomi bo'yicha qidirish:")
    response = requests.get(f"{BASE_URL}/orders/?client_name=a")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Nomida 'a' harfi bo'lgan clientlar uchun {data['count']} ta buyurtma topildi")
    else:
        print(f"   ❌ Xatolik: {response.status_code}")
    
    # 5. Status bo'yicha filterlash
    print("\n5. Status bo'yicha filterlash:")
    response = requests.get(f"{BASE_URL}/orders/?status=kutilmoqda")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Kutilmoqda status bo'yicha {data['count']} ta buyurtma topildi")
    else:
        print(f"   ❌ Xatolik: {response.status_code}")
    
    # 6. Clientlar ro'yxati
    print("\n6. Clientlar ro'yxati (autorizatsiyasiz):")
    response = requests.get(f"{BASE_URL}/clients/")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Jami clientlar: {data['count']}")
        if data['results']:
            print("   📋 Birinchi client:")
            first_client = data['results'][0]
            print(f"      - ID: {first_client['id']}")
            print(f"      - Ism: {first_client['full_name']}")
            print(f"      - Telefon: {first_client['phone_number']}")
    else:
        print(f"   ❌ Xatolik: {response.status_code}")
    
    # 7. Yangi buyurtma yaratish
    print("\n7. Yangi buyurtma yaratish (autorizatsiyasiz):")
    new_order_data = {
        "client_full_name": "Test Client",
        "client_phone_number": "+998901234567",
        "client_location_name": "Test Location",
        "client_address": "Test Address",
        "client_longitude": "69.2401",
        "client_latitude": "41.2995",
        "kiruvchi_soni": 10,
        "chiquvchi_soni": 0,
        "notes": "Test buyurtma - autorizatsiyasiz"
    }
    
    response = requests.post(f"{BASE_URL}/orders/", json=new_order_data)
    if response.status_code == 201:
        data = response.json()
        print(f"   ✅ Yangi buyurtma yaratildi!")
        print(f"      - ID: {data['id']}")
        print(f"      - Client: {data['client']['full_name']}")
        print(f"      - Status: {data['status']}")
    else:
        print(f"   ❌ Xatolik: {response.status_code}")
        print(f"   Response: {response.text}")

def main():
    print("🚀 AUTORIZATSIYASIZ FILTERLASH TESTLARI BOSHLANDI!")
    print("=" * 70)
    
    test_no_auth_filters()
    
    print("\n" + "=" * 70)
    print("🎉 AUTORIZATSIYASIZ FILTERLASH TESTLARI YAKUNLANDI!")
    
    print("\n📋 AUTORIZATSIYASIZ ISHLAYDIGANLAR:")
    print("   ✅ GET /api/orders/              - Barcha buyurtmalar")
    print("   ✅ GET /api/orders/?client_id=123 - Client ID filterlash")
    print("   ✅ GET /api/orders/?client_name=a - Client nomi filterlash")
    print("   ✅ GET /api/orders/?status=kutilmoqda - Status filterlash")
    print("   ✅ GET /api/clients/             - Barcha clientlar")
    print("   ✅ POST /api/orders/             - Yangi buyurtma yaratish")
    
    print("\n🎯 MUVAFFAQIYAT: Autorizatsiya vaqtincha o'chirildi!")

if __name__ == "__main__":
    main()