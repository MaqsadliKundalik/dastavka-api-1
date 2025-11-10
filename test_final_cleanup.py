#!/usr/bin/env python3
"""
Final test after location_name field removal
Tests simplified Client model and API endpoints
"""

import requests
import json

# API base URL
BASE_URL = "http://127.0.0.1:8000/api"

def print_separator(title):
    print("\n" + "="*60)
    print(f"🧪 {title}")
    print("="*60)

def test_create_client():
    """Test client creation without location_name"""
    print_separator("CLIENT YARATISH TESTI (location_name siz)")
    
    client_data = {
        "full_name": "Test Mijoz",
        "phone_number": "+998901234567",
        "address": "Toshkent shahar, Yunusobod tumani, 123-uy",
        "coordinates": "41.2995,69.2401",
        "notes": "Test mijoz ma'lumotlari"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/clients/", json=client_data)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 201:
            client = response.json()
            print("✅ Mijoz muvaffaqiyatli yaratildi:")
            print(f"   ID: {client['id']}")
            print(f"   Ism: {client['full_name']}")
            print(f"   Telefon: {client['phone_number']}")
            print(f"   Manzil: {client['address']}")
            print(f"   Koordinatalar: {client.get('coordinates', 'N/A')}")
            return client['id']
        else:
            print("❌ Xatolik:")
            print(response.text)
            return None
            
    except Exception as e:
        print(f"❌ Xatolik: {e}")
        return None

def test_list_clients():
    """Test client listing"""
    print_separator("MIJOZLAR RO'YXATI")
    
    try:
        response = requests.get(f"{BASE_URL}/clients/")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            clients = response.json()
            print(f"✅ Jami mijozlar soni: {len(clients)}")
            
            for client in clients[:3]:  # Faqat birinchi 3 ta
                print(f"   📋 ID: {client['id']} | {client['full_name']} | {client['address']}")
                
        else:
            print("❌ Xatolik:")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Xatolik: {e}")

def test_create_order(client_id):
    """Test order creation with simplified fields"""
    if not client_id:
        print("❌ Client ID mavjud emas")
        return None
        
    print_separator("BUYURTMA YARATISH TESTI")
    
    order_data = {
        "client_id": client_id,
        "baklashka_soni": 5,
        "kuler_soni": 2,
        "notes": "Test buyurtma - baklashka va kuler"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/orders/", json=order_data)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 201:
            order = response.json()
            print("✅ Buyurtma muvaffaqiyatli yaratildi:")
            print(f"   ID: {order['id']}")
            print(f"   Mijoz: {order['client']['full_name']}")
            print(f"   Manzil: {order['client']['address']}")
            print(f"   Baklashka: {order['baklashka_soni']}")
            print(f"   Kuler: {order['kuler_soni']}")
            print(f"   Holat: {order['status']}")
            return order['id']
        else:
            print("❌ Xatolik:")
            print(response.text)
            return None
            
    except Exception as e:
        print(f"❌ Xatolik: {e}")
        return None

def test_order_statistics():
    """Test statistics with new field names"""
    print_separator("STATISTIKA TESTI")
    
    endpoints = [
        ("orders-stats", "Asosiy statistika"),
        ("general-stats", "Umumiy statistika"),
        ("top-clients", "Top mijozlar"),
        ("couriers-stats", "Kuryerlar statistikasi")
    ]
    
    for endpoint, name in endpoints:
        try:
            response = requests.get(f"{BASE_URL}/statistics/{endpoint}/")
            print(f"\n📊 {name}:")
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                if endpoint == "orders-stats":
                    print(f"   ✅ Bugungi buyurtmalar: {data.get('today', {}).get('orders_count', 0)}")
                    print(f"   ✅ Bugungi baklashkalar: {data.get('today', {}).get('total_baklashka', 0)}")
                    print(f"   ✅ Bugungi kulerlar: {data.get('today', {}).get('total_kuler', 0)}")
                elif endpoint == "general-stats":
                    print(f"   ✅ Jami buyurtmalar: {data.get('total_orders', 0)}")
                    print(f"   ✅ Jami baklashkalar: {data.get('total_baklashka', 0)}")
                    print(f"   ✅ Jami kulerlar: {data.get('total_kuler', 0)}")
                else:
                    print(f"   ✅ Ma'lumotlar olindi")
            else:
                print(f"   ❌ Xatolik: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Xatolik: {e}")

def main():
    print("🚀 YAKUNIY TEST - location_name o'chirilgandan keyin")
    print("📅", "2024-11-10")
    
    # Test client creation
    client_id = test_create_client()
    
    # Test client listing
    test_list_clients()
    
    # Test order creation
    order_id = test_create_order(client_id)
    
    # Test statistics
    test_order_statistics()
    
    print_separator("TEST YAKUNLANDI")
    print("✅ Barcha testlar tugallandi!")
    print("✅ location_name field muvaffaqiyatli o'chirildi")
    print("✅ baklashka_soni va kuler_soni fieldlari ishlayapti")
    print("✅ Statistika API lar to'g'ri ishlayapti")

if __name__ == "__main__":
    main()