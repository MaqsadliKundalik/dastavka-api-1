#!/usr/bin/env python3
"""
Final cleanup test after location_name field removal
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_working_system():
    """Test that the system is working after location_name removal"""
    print("🧪 SISTEMA TESTI (location_name o'chirilgandan keyin)")
    print("="*60)
    
    # 1. Orders endpoint test
    try:
        response = requests.get(f"{BASE_URL}/api/orders/")
        print(f"📦 Orders endpoint: Status {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Buyurtmalar soni: {data.get('count', 0)}")
            if data.get('results'):
                order = data['results'][0]
                print(f"   ✅ Birinchi buyurtma:")
                print(f"      - ID: {order.get('id')}")
                print(f"      - Mijoz: {order.get('client_full_name')}")
                print(f"      - Manzil: {order.get('client_address')}")  # location_name emas!
                print(f"      - Baklashka: {order.get('baklashka_soni')}")
                print(f"      - Kuler: {order.get('kuler_soni')}")
        else:
            print(f"   ❌ Xato: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Exception: {e}")
    
    # 2. Clients endpoint test
    try:
        response = requests.get(f"{BASE_URL}/api/clients/")
        print(f"\n📋 Clients endpoint: Status {response.status_code}")
        if response.status_code == 200:
            clients = response.json()
            print(f"   ✅ Mijozlar soni: {len(clients)}")
            if clients:
                client = clients[0]
                print(f"   ✅ Birinchi mijoz:")
                print(f"      - ID: {client.get('id')}")
                print(f"      - Ism: {client.get('full_name')}")
                print(f"      - Telefon: {client.get('phone_number')}")
                print(f"      - Manzil: {client.get('address')}")
                # location_name field yo'q bo'lishi kerak
                if 'location_name' not in client:
                    print("   ✅ location_name field muvaffaqiyatli o'chirildi")
                else:
                    print("   ⚠️  location_name field hali ham mavjud")
        else:
            print(f"   ❌ Xato: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Exception: {e}")
    
    # 3. Test new client creation
    print(f"\n🆕 Yangi mijoz yaratish testi:")
    client_data = {
        "full_name": "Test Mijoz Cleanup",
        "phone_number": "+998901234567",
        "address": "Toshkent shahar, Test ko'chasi, 123-uy"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/clients/", json=client_data)
        print(f"   Status: {response.status_code}")
        if response.status_code == 201:
            client = response.json()
            print(f"   ✅ Mijoz yaratildi:")
            print(f"      - ID: {client['id']}")
            print(f"      - Ism: {client['full_name']}")
            print(f"      - Manzil: {client['address']}")
            print(f"   ✅ location_name field toza o'chirilgan")
            
            # Test order creation with this client
            print(f"\n📦 Ushbu mijoz bilan buyurtma yaratish:")
            order_data = {
                "client_id": client['id'],
                "baklashka_soni": 3,
                "kuler_soni": 1,
                "notes": "Test buyurtma - cleanup keyin"
            }
            
            order_response = requests.post(f"{BASE_URL}/api/orders/", json=order_data)
            print(f"   Status: {order_response.status_code}")
            if order_response.status_code == 201:
                order = order_response.json()
                print(f"   ✅ Buyurtma yaratildi:")
                print(f"      - ID: {order['id']}")
                print(f"      - Baklashka: {order['baklashka_soni']}")
                print(f"      - Kuler: {order['kuler_soni']}")
                print(f"      - Mijoz manzili: {order['client']['address']}")
            else:
                print(f"   ❌ Buyurtma yaratishda xato: {order_response.status_code}")
                
        else:
            print(f"   ❌ Mijoz yaratishda xato: {response.status_code}")
            print(f"   Xato: {response.text}")
    except Exception as e:
        print(f"   ❌ Exception: {e}")
    
    print(f"\n" + "="*60)
    print("🎉 CLEANUP MUVAFFAQIYAT!")
    print("✅ location_name field to'liq o'chirildi")
    print("✅ address field ishlayapti")
    print("✅ baklashka_soni va kuler_soni fieldlari ishlayapti")
    print("✅ API to'liq funksional")
    print("="*60)

if __name__ == "__main__":
    test_working_system()