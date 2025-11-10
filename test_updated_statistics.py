#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000/api"

def test_order_statistics():
    print("📊 BUYURTMALAR STATISTIKASI TESTLARI!")
    print("🚀 BAKLASHKA VA KULER BILAN STATISTIKA")
    print("=" * 60)
    
    # 1. Bugungi statistika
    print("\n1. Bugungi statistika:")
    try:
        response = requests.get(f"{BASE_URL}/orders/stats/?period=today")
        print(f"   📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            stats = response.json()
            summary = stats.get('summary', {})
            
            print(f"   ✅ BUGUNGI STATISTIKA:")
            print(f"      📋 Davr: {summary.get('period')}")
            print(f"      🔢 Jami buyurtmalar: {summary.get('total_orders')}")
            print(f"      ⏳ Kutilayotgan: {summary.get('pending_orders')}")
            print(f"      🔄 Jarayonda: {summary.get('in_progress_orders')}")
            print(f"      ✅ Yakunlangan: {summary.get('completed_orders')}")
            print(f"      ❌ Bekor qilingan: {summary.get('cancelled_orders')}")
            print(f"      🏺 Jami baklashkalar: {summary.get('total_baklashka')}")
            print(f"      🚰 Jami kulerlar: {summary.get('total_kuler')}")
            
            # Kunlik taqsimot
            daily = stats.get('daily_breakdown', [])
            if daily:
                print(f"   📅 Kunlik taqsimot: {len(daily)} kun")
                for day in daily[:3]:  # Faqat birinchi 3 ta kun
                    print(f"      {day.get('date')}: {day.get('total_orders')} buyurtma, 🏺{day.get('total_baklashka')} baklashka, 🚰{day.get('total_kuler')} kuler")
        else:
            print(f"   ❌ XATOLIK: {response.text}")
    except Exception as e:
        print(f"   ⚠️ CONNECTION ERROR: {e}")
    
    # 2. Haftalik statistika
    print("\n2. Haftalik statistika:")
    try:
        response = requests.get(f"{BASE_URL}/orders/stats/?period=week")
        print(f"   📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            stats = response.json()
            summary = stats.get('summary', {})
            
            print(f"   ✅ HAFTALIK STATISTIKA:")
            print(f"      📋 Davr: {summary.get('period')}")
            print(f"      🔢 Jami buyurtmalar: {summary.get('total_orders')}")
            print(f"      ✅ Yakunlangan: {summary.get('completed_orders')}")
            print(f"      🏺 Jami baklashkalar: {summary.get('total_baklashka')}")
            print(f"      🚰 Jami kulerlar: {summary.get('total_kuler')}")
            
            # Kunlik taqsimot
            daily = stats.get('daily_breakdown', [])
            print(f"   📅 Kunlik taqsimot: {len(daily)} kun")
        else:
            print(f"   ❌ XATOLIK: {response.text}")
    except Exception as e:
        print(f"   ⚠️ CONNECTION ERROR: {e}")
    
    # 3. Oylik statistika  
    print("\n3. Oylik statistika:")
    try:
        response = requests.get(f"{BASE_URL}/orders/stats/?period=month")
        print(f"   📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            stats = response.json()
            summary = stats.get('summary', {})
            
            print(f"   ✅ OYLIK STATISTIKA:")
            print(f"      📋 Davr: {summary.get('period')}")
            print(f"      🔢 Jami buyurtmalar: {summary.get('total_orders')}")
            print(f"      ✅ Yakunlangan: {summary.get('completed_orders')}")
            print(f"      🏺 Jami baklashkalar: {summary.get('total_baklashka')}")
            print(f"      🚰 Jami kulerlar: {summary.get('total_kuler')}")
            
            # Kunlik taqsimot
            daily = stats.get('daily_breakdown', [])
            print(f"   📅 Kunlik taqsimot: {len(daily)} kun")
            
            # Oxirgi bir necha kunni ko'rsatamiz
            if daily and len(daily) > 3:
                print(f"   📈 Oxirgi kunlar:")
                for day in daily[-3:]:
                    print(f"      {day.get('date')}: {day.get('total_orders')} buyurtma, 🏺{day.get('total_baklashka')} baklashka, 🚰{day.get('total_kuler')} kuler")
        else:
            print(f"   ❌ XATOLIK: {response.text}")
    except Exception as e:
        print(f"   ⚠️ CONNECTION ERROR: {e}")
    
    # 4. Umumiy statistika
    print("\n4. Umumiy statistika:")
    try:
        response = requests.get(f"{BASE_URL}/orders/stats/general/")
        print(f"   📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            stats = response.json()
            
            print(f"   ✅ UMUMIY STATISTIKA:")
            print(f"      📋 Davr: {stats.get('period')}")
            print(f"      🔢 Jami buyurtmalar: {stats.get('total_orders')}")
            print(f"      ⏳ Kutilayotgan: {stats.get('pending_orders')}")
            print(f"      🔄 Jarayonda: {stats.get('in_progress_orders')}")
            print(f"      ✅ Yakunlangan: {stats.get('completed_orders')}")
            print(f"      ❌ Bekor qilingan: {stats.get('cancelled_orders')}")
            print(f"      🏺 Jami baklashkalar: {stats.get('total_baklashka')}")
            print(f"      🚰 Jami kulerlar: {stats.get('total_kuler')}")
            
            # Yakunlangan foiz
            total = stats.get('total_orders', 0)
            completed = stats.get('completed_orders', 0)
            if total > 0:
                completion_rate = (completed / total) * 100
                print(f"      📈 Yakunlash darajasi: {completion_rate:.1f}%")
                
            # Baklashka va kuler foizlari
            total_baklashka = stats.get('total_baklashka', 0)
            total_kuler = stats.get('total_kuler', 0)
            if total_baklashka or total_kuler:
                print(f"      📊 Baklashka/Kuler nisbati: {total_baklashka}:{total_kuler}")
        else:
            print(f"   ❌ XATOLIK: {response.text}")
    except Exception as e:
        print(f"   ⚠️ CONNECTION ERROR: {e}")

    print("\n" + "=" * 60)
    print("🎉 YANGILANGAN STATISTIKA TESTLARI YAKUNLANDI!")
    
    print("\n📋 MAVJUD ENDPOINT-LAR:")
    print("✅ STATISTIKA API-LARI (YANGILANGAN):")
    print("   - GET /api/orders/stats/?period=today - Bugungi statistika")
    print("   - GET /api/orders/stats/?period=week - Haftalik statistika")
    print("   - GET /api/orders/stats/?period=month - Oylik statistika")
    print("   - GET /api/orders/stats/general/ - Umumiy statistika")
    print("\n🏺 BAKLASHKA VA 🚰 KULER FIELDLARI QO'SHILDI!")

if __name__ == "__main__":
    test_order_statistics()