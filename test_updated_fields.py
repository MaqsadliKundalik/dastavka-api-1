#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def test_updated_order_fields():
    print("🔄 YANGILANGAN BUYURTMA FIELDLARI TESTLARI!")
    print("🏺 BAKLASHKA VA KULER FIELDLARI BILAN")
    print("=" * 60)
    
    # 1. Mavjud clientlar ro'yxati
    print("\n1. Mavjud clientlar ro'yxati:")
    try:
        response = requests.get(f"{BASE_URL}/clients/")
        print(f"   📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            response_data = response.json()
            if isinstance(response_data, dict) and 'results' in response_data:
                clients = response_data['results']
                total_count = response_data.get('count', len(clients))
                print(f"   📋 Jami clientlar: {total_count}")
            else:
                clients = response_data if isinstance(response_data, list) else []
                print(f"   📋 Jami clientlar: {len(clients)}")
            
            if clients:
                first_three = clients[:3] if len(clients) > 3 else clients
                for i, client in enumerate(first_three, 1):
                    print(f"   {i}. ID: {client.get('id')} - {client.get('full_name')} ({client.get('phone_number')})")
                
                # Test uchun birinchi clientni tanlaymiz
                test_client = clients[0]
                client_id = test_client.get('id')
                
                print(f"\n2. Test uchun Client ID {client_id} tanlandı:")
                print(f"   👤 Ism: {test_client.get('full_name')}")
                print(f"   📞 Telefon: {test_client.get('phone_number')}")
                
                # 3. Yangi fieldlar bilan buyurtma yaratish
                print(f"\n3. Baklashka va kuler bilan buyurtma yaratish:")
                order_data = {
                    "client_id": client_id,
                    "baklashka_soni": 15,
                    "kuler_soni": 3,
                    "notes": "Yangi fieldlar bilan test buyurtma"
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
                    print(f"      🏺 Baklashkalar: {result.get('baklashka_soni')}")
                    print(f"      🚰 Kulerlar: {result.get('kuler_soni')}")
                    print(f"      📝 Izoh: {result.get('notes')}")
                    
                    # Yangi yaratilgan buyurtma ID sini saqlaymiz
                    new_order_id = result.get('id')
                    
                    # 4. Yaratilgan buyurtmani tekshirish
                    print(f"\n4. Yaratilgan buyurtmani tekshirish:")
                    response = requests.get(f"{BASE_URL}/orders/{new_order_id}/")
                    print(f"   📊 Status: {response.status_code}")
                    
                    if response.status_code == 200:
                        order_detail = response.json()
                        print(f"   ✅ Buyurtma ma'lumotlari:")
                        print(f"      🆔 ID: {order_detail.get('id')}")
                        print(f"      🏺 Baklashka: {order_detail.get('baklashka_soni')}")
                        print(f"      🚰 Kuler: {order_detail.get('kuler_soni')}")
                        print(f"      📊 Status: {order_detail.get('status')}")
                    else:
                        print(f"   ❌ XATOLIK: {response.text}")
                
                else:
                    print(f"   ❌ XATOLIK: {response.text}")
            
            else:
                print("      ⚠️ Clientlar ro'yxati bo'sh!")
        else:
            print(f"   ❌ XATOLIK: {response.text}")
            
    except Exception as e:
        print(f"   ⚠️ CONNECTION ERROR: {e}")

    print("\n" + "=" * 60)
    print("🎉 YANGILANGAN FIELDLAR TESTLARI YAKUNLANDI!")
    
    print("\n📋 YANGILANGAN FIELDLAR:")
    print("✅ BUYURTMA YARATISH:")
    print("   - client_id (majburiy)")
    print("   - baklashka_soni (ixtiyoriy, default: 0)")
    print("   - kuler_soni (ixtiyoriy, default: 0)")
    print("   - notes (ixtiyoriy)")
    print("   - assigned_to (ixtiyoriy)")

if __name__ == "__main__":
    test_updated_order_fields()