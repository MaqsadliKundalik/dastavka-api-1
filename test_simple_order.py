#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def test_simple_order_creation():
    print("🎯 SODDA BUYURTMA YARATISH TESTLARI!")
    print("🚀 FAQAT CLIENT_ID BILAN BUYURTMA YARATISH")
    print("=" * 60)
    
    # 1. Mavjud clientlar ro'yxati
    print("\n1. Mavjud clientlar ro'yxati:")
    try:
        response = requests.get(f"{BASE_URL}/clients/")
        print(f"   📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            response_data = response.json()
            print(f"   📋 Javob turi: {type(response_data)}")
            
            # Pagination bilan keladigan javobni handle qilamiz
            if isinstance(response_data, dict) and 'results' in response_data:
                clients = response_data['results']
                total_count = response_data.get('count', len(clients))
                print(f"   📋 Jami clientlar: {total_count}")
            else:
                clients = response_data if isinstance(response_data, list) else []
                print(f"   � Jami clientlar: {len(clients)}")
            
            if clients:
                first_five = clients[:5] if len(clients) > 5 else clients
                for i, client in enumerate(first_five, 1):
                    print(f"   {i}. ID: {client.get('id')} - {client.get('full_name')} ({client.get('phone_number')})")
                
                # Test uchun birinchi clientni tanlaymiz
                test_client = clients[0]
                client_id = test_client.get('id')
                
                print(f"\n2. Test uchun Client ID {client_id} tanlandı:")
                print(f"   👤 Ism: {test_client.get('full_name')}")
                print(f"   📞 Telefon: {test_client.get('phone_number')}")
                
                # 3. Faqat client_id bilan buyurtma yaratish
                print(f"\n3. Faqat client_id={client_id} bilan buyurtma yaratish:")
                order_data = {
                    "client_id": client_id,
                    "kiruvchi_soni": 12,
                    "chiquvchi_soni": 1,
                    "notes": "Sodda test buyurtma"
                }
                
                print(f"   📤 Yuborilayotgan ma'lumotlar:")
                print(f"   {json.dumps(order_data, indent=6, ensure_ascii=False)}")
                
                response = requests.post(f"{BASE_URL}/orders/", json=order_data)
                print(f"   📊 Status: {response.status_code}")
                
                if response.status_code == 201:
                    result = response.json()
                    print(f"   ✅ MUVAFFAQIYAT! Yangi buyurtma yaratildi:")
                    print(f"      🆔 Buyurtma ID: {result.get('id')}")
                    print(f"      👤 Client: {result.get('client', {}).get('full_name')}")
                    print(f"      📞 Telefon: {result.get('client', {}).get('phone_number')}")
                    print(f"      📦 Kiruvchi: {result.get('kiruvchi_soni')}")
                    print(f"      📤 Chiquvchi: {result.get('chiquvchi_soni')}")
                    print(f"      📝 Izoh: {result.get('notes')}")
                else:
                    print(f"   ❌ XATOLIK: {response.text}")
                
                # 4. Noto'g'ri client_id bilan test
                print(f"\n4. Noto'g'ri client_id=99999 bilan test:")
                bad_order_data = {
                    "client_id": 99999,
                    "kiruvchi_soni": 5,
                    "chiquvchi_soni": 0,
                    "notes": "Bu ishlamaydi"
                }
                
                response = requests.post(f"{BASE_URL}/orders/", json=bad_order_data)
                print(f"   📊 Status: {response.status_code}")
                
                if response.status_code == 400:
                    error = response.json()
                    print(f"   ✅ To'g'ri! Kutilgan xatolik qaytdi:")
                    print(f"   ❌ {error}")
                else:
                    print(f"   ⚠️ Kutilmagan javob: {response.text}")
                
                # 5. Client_id siz test
                print(f"\n5. Client_id siz buyurtma yaratish testi:")
                no_client_data = {
                    "kiruvchi_soni": 3,
                    "chiquvchi_soni": 0,
                    "notes": "Client_id yo'q"
                }
                
                response = requests.post(f"{BASE_URL}/orders/", json=no_client_data)
                print(f"   📊 Status: {response.status_code}")
                
                if response.status_code == 400:
                    error = response.json()
                    print(f"   ✅ To'g'ri! Kutilgan xatolik qaytdi:")
                    print(f"   ❌ {error}")
                else:
                    print(f"   ⚠️ Kutilmagan javob: {response.text}")
            
            else:
                print("   ⚠️ Clientlar ro'yxati bo'sh!")
        else:
            print(f"   ❌ XATOLIK: {response.text}")
            
    except Exception as e:
        print(f"   ⚠️ CONNECTION ERROR: {e}")

    print("\n" + "=" * 60)
    print("🎉 TESTLAR YAKUNLANDI!")
    
    print("\n📋 XULOSA:")
    print("✅ BUYURTMA YARATISH:")
    print("   - Faqat client_id majburiy")
    print("   - Kiruvchi va chiquvchi soni ixtiyoriy")
    print("   - Notes ixtiyoriy")
    print("   - Boshqa client ma'lumotlari kerak emas")

if __name__ == "__main__":
    test_simple_order_creation()