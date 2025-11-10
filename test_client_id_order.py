#!/usr/bin/env python
"""
Client ID bo'yicha buyurtma yaratishni test qilish
"""

import requests
import json

# Base URL
BASE_URL = "http://localhost:8000/api"

def test_order_with_client_id():
    """Client ID bo'yicha buyurtma yaratishni test qilish"""
    
    print("🚀 CLIENT ID BILAN BUYURTMA YARATISH TESTLARI")
    print("=" * 60)
    
    # 1. Avval mavjud clientlarni ko'ramiz
    print("\n1. Mavjud clientlar ro'yxati:")
    response = requests.get(f"{BASE_URL}/clients/")
    if response.status_code == 200:
        clients = response.json()['results']
        print(f"   📋 Jami clientlar: {len(clients)}")
        
        if clients:
            for i, client in enumerate(clients[:5], 1):
                print(f"   {i}. ID: {client['id']} - {client['full_name']} ({client['phone_number']})")
            
            # Test uchun birinchi clientni tanlaymiz
            test_client = clients[0]
            client_id = test_client['id']
            client_name = test_client['full_name']
            client_phone = test_client['phone_number']
            
            print(f"\n2. Test uchun Client ID {client_id} tanlandı:")
            print(f"   👤 Ism: {client_name}")
            print(f"   📞 Telefon: {client_phone}")
            
            # 3. Faqat client_id bilan buyurtma yaratish
            print(f"\n3. Faqat client_id={client_id} bilan buyurtma yaratish:")
            order_data = {
                "client_id": client_id,
                "kiruvchi_soni": 15,
                "chiquvchi_soni": 2,
                "notes": "Client ID bilan yaratilgan test buyurtma"
            }
            
            print(f"   📤 Yuborilayotgan ma'lumotlar:")
            print(f"   {json.dumps(order_data, indent=6, ensure_ascii=False)}")
            
            response = requests.post(f"{BASE_URL}/orders/", json=order_data)
            
            if response.status_code == 201:
                new_order = response.json()
                print(f"\n   ✅ MUVAFFAQIYAT! Yangi buyurtma yaratildi:")
                print(f"      🆔 Buyurtma ID: {new_order['id']}")
                print(f"      👤 Client ID: {new_order['client']['id']}")
                print(f"      👤 Client nomi: {new_order['client']['full_name']}")
                print(f"      📞 Client telefon: {new_order['client']['phone_number']}")
                print(f"      📍 Manzil: {new_order['client']['address']}")
                print(f"      📦 Kiruvchi: {new_order.get('kiruvchi_soni', 'N/A')}")
                print(f"      📤 Chiquvchi: {new_order.get('chiquvchi_soni', 'N/A')}")
                print(f"      📝 Izoh: {new_order.get('notes', 'N/A')}")
                
                return new_order['id']
            else:
                print(f"   ❌ XATOLIK: {response.status_code}")
                print(f"   Response: {response.text}")
                return None
        else:
            print("   ⚠️ Hech qanday client topilmadi!")
            return None
    else:
        print(f"   ❌ Clientlarni olishda xatolik: {response.status_code}")
        return None

def test_order_with_new_client():
    """Yangi client ma'lumotlari bilan buyurtma yaratish"""
    print("\n4. Yangi client ma'lumotlari bilan buyurtma yaratish:")
    
    order_data = {
        "client_full_name": "Test Client - Yangi",
        "client_phone_number": "+998901111111",
        "client_location_name": "Test Location",
        "client_address": "Test Address, Toshkent",
        "client_longitude": "69.2401",
        "client_latitude": "41.2995",
        "kiruvchi_soni": 8,
        "chiquvchi_soni": 0,
        "notes": "Yangi client bilan yaratilgan test buyurtma"
    }
    
    print(f"   📤 Yuborilayotgan ma'lumotlar:")
    print(f"   {json.dumps(order_data, indent=6, ensure_ascii=False)}")
    
    response = requests.post(f"{BASE_URL}/orders/", json=order_data)
    
    if response.status_code == 201:
        new_order = response.json()
        print(f"\n   ✅ MUVAFFAQIYAT! Yangi client va buyurtma yaratildi:")
        print(f"      🆔 Buyurtma ID: {new_order['id']}")
        print(f"      👤 Yangi Client ID: {new_order['client']['id']}")
        print(f"      👤 Client nomi: {new_order['client']['full_name']}")
        print(f"      📞 Client telefon: {new_order['client']['phone_number']}")
        
        return new_order['id']
    else:
        print(f"   ❌ XATOLIK: {response.status_code}")
        print(f"   Response: {response.text}")
        return None

def test_invalid_client_id():
    """Mavjud bo'lmagan client ID bilan test"""
    print("\n5. Mavjud bo'lmagan client ID bilan test:")
    
    order_data = {
        "client_id": 99999,  # Mavjud bo'lmagan ID
        "kiruvchi_soni": 5,
        "chiquvchi_soni": 0,
        "notes": "Noto'g'ri client ID bilan test"
    }
    
    response = requests.post(f"{BASE_URL}/orders/", json=order_data)
    
    if response.status_code == 400:
        error = response.json()
        print(f"   ✅ To'g'ri! Kutilgan xatolik qaytdi:")
        print(f"   ❌ {error}")
    else:
        print(f"   ⚠️ Kutilmagan natija: {response.status_code}")
        print(f"   Response: {response.text}")

def main():
    print("🎯 CLIENT ID BILAN BUYURTMA YARATISH TESTLARI BOSHLANDI!")
    
    # 1. Client ID bilan buyurtma yaratish
    order_id_1 = test_order_with_client_id()
    
    # 2. Yangi client bilan buyurtma yaratish
    order_id_2 = test_order_with_new_client()
    
    # 3. Noto'g'ri client ID bilan test
    test_invalid_client_id()
    
    print("\n" + "=" * 60)
    print("🎉 TESTLAR YAKUNLANDI!")
    
    print("\n📋 XULOSA:")
    print("✅ CLIENT ID USULI:")
    print("   - Faqat client_id kiritasiz")
    print("   - Client ma'lumotlari avtomatik olinadi")
    print("   - Tezroq va sodda")
    
    print("\n✅ YANGI CLIENT USULI:")
    print("   - To'liq client ma'lumotlarini kiritasiz")
    print("   - Yangi client avtomatik yaratiladi")
    print("   - Birinchi marta kelgan mijozlar uchun")
    
    print(f"\n🎯 YARATILGAN BUYURTMALAR:")
    if order_id_1:
        print(f"   - Client ID bilan: #{order_id_1}")
    if order_id_2:
        print(f"   - Yangi client bilan: #{order_id_2}")

if __name__ == "__main__":
    main()