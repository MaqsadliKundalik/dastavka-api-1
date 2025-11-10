#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def test_advanced_statistics():
    print("📊 QO'SHIMCHA STATISTIKA TESTLARI!")
    print("🔥 ENG FAOL MIJOZLAR VA KURYERLAR (YANGILANGAN)")
    print("=" * 60)
    
    # 1. Eng faol mijozlar - shu oy
    print("\n1. Eng faol mijozlar (shu oy):")
    try:
        response = requests.get(f"{BASE_URL}/orders/stats/top-clients/?period=month&limit=5")
        print(f"   📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"   ✅ ENG FAOL MIJOZLAR:")
            print(f"      📋 Davr: {data.get('period')}")
            
            clients = data.get('top_clients', [])
            if clients:
                print(f"      👥 Jami mijozlar: {len(clients)}")
                for i, client in enumerate(clients, 1):
                    print(f"      {i}. {client.get('client_name')} (ID: {client.get('client_id')})")
                    print(f"         📞 {client.get('client_phone')}")
                    print(f"         🔢 Buyurtmalar: {client.get('total_orders')}")
                    print(f"         🏺 Baklashkalar: {client.get('total_baklashka')}, 🚰 Kulerlar: {client.get('total_kuler')}")
                    print(f"         📅 Oxirgi buyurtma: {client.get('last_order_date')}")
                    print()
            else:
                print("      ⚠️ Faol mijozlar topilmadi")
        else:
            print(f"   ❌ XATOLIK: {response.text}")
    except Exception as e:
        print(f"   ⚠️ CONNECTION ERROR: {e}")
    
    # 2. Eng faol mijozlar - barcha vaqt
    print("\n2. Eng faol mijozlar (barcha vaqt):")
    try:
        response = requests.get(f"{BASE_URL}/orders/stats/top-clients/?period=all&limit=3")
        print(f"   📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"   ✅ BARCHA VAQT ENG FAOL MIJOZLAR:")
            print(f"      📋 Davr: {data.get('period')}")
            
            clients = data.get('top_clients', [])
            if clients:
                for i, client in enumerate(clients, 1):
                    print(f"      🥇 TOP-{i}: {client.get('client_name')}")
                    print(f"         🔢 {client.get('total_orders')} buyurtma")
                    print(f"         🏺 {client.get('total_baklashka')} baklashka, 🚰 {client.get('total_kuler')} kuler")
            else:
                print("      ⚠️ Mijozlar topilmadi")
        else:
            print(f"   ❌ XATOLIK: {response.text}")
    except Exception as e:
        print(f"   ⚠️ CONNECTION ERROR: {e}")
    
    # 3. Kuryerlar statistikasi
    print("\n3. Kuryerlar statistikasi:")
    try:
        response = requests.get(f"{BASE_URL}/orders/stats/couriers/?period=month")
        print(f"   📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"   ✅ KURYERLAR STATISTIKASI:")
            print(f"      📋 Davr: {data.get('period')}")
            
            couriers = data.get('couriers_stats', [])
            if couriers:
                print(f"      🚚 Jami kuryerlar: {len(couriers)}")
                
                # Faqat faol kuryerlarni ko'rsatamiz (tayinlangan buyurtmalari bor)
                active_couriers = [c for c in couriers if c.get('assigned_orders', 0) > 0]
                
                if active_couriers:
                    print(f"      🔥 Faol kuryerlar: {len(active_couriers)}")
                    for i, courier in enumerate(active_couriers, 1):
                        print(f"      {i}. {courier.get('courier_name')} (@{courier.get('courier_username')})")
                        print(f"         📋 Tayinlangan: {courier.get('assigned_orders')}")
                        print(f"         ✅ Yakunlangan: {courier.get('completed_orders')}")
                        print(f"         🔄 Jarayonda: {courier.get('in_progress_orders')}")
                        print(f"         📈 Yakunlash darajasi: {courier.get('completion_rate')}%")
                        print()
                else:
                    print("      ⚠️ Faol kuryerlar yo'q (hech kimga buyurtma tayinlanmagan)")
                
                # Faoliyatsiz kuryerlar
                inactive_count = len(couriers) - len(active_couriers)
                if inactive_count > 0:
                    print(f"      😴 Faoliyatsiz kuryerlar: {inactive_count}")
                    
            else:
                print("      ⚠️ Kuryerlar topilmadi")
        else:
            print(f"   ❌ XATOLIK: {response.text}")
    except Exception as e:
        print(f"   ⚠️ CONNECTION ERROR: {e}")

    print("\n" + "=" * 60)
    print("🎉 YANGILANGAN QO'SHIMCHA STATISTIKA TESTLARI YAKUNLANDI!")
    
    print("\n📋 YANGI ENDPOINT-LAR:")
    print("✅ QO'SHIMCHA STATISTIKA API-LARI:")
    print("   - GET /api/orders/stats/top-clients/?period=month&limit=10 - Eng faol mijozlar")
    print("   - GET /api/orders/stats/couriers/?period=month - Kuryerlar statistikasi")
    print("   - period: today, week, month, all")
    print("\n🏺 BAKLASHKA VA 🚰 KULER BILAN YANGILANDI!")

if __name__ == "__main__":
    test_advanced_statistics()