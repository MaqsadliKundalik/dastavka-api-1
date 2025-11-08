#!/usr/bin/env python3
import requests
import json

TOKEN = "0e67507b8fdbe16192d16d81c8ccea6eec889312"
BASE_URL = "http://127.0.0.1:8000/api"

def test_new_order_format():
    """Yangi buyumlar soni format bilan order yaratish"""
    print("🆕 Yangi order format testi...")
    
    headers = {
        "Authorization": f"Token {TOKEN}",
        "Content-Type": "application/json"
    }
    
    # Yangi format bilan order yaratish
    order_data = {
        "full_name": "Aziz Karimov",
        "phone_number": "+998901111111",
        "address": "Toshkent, Mirobod tumani, 22-uy",
        "kiruvchi_soni": 8,
        "chiquvchi_soni": 3,
        "notes": "Kiruvchi: 8 ta buyum, Chiquvchi: 3 ta buyum",
        "longitude": "69.250000",
        "latitude": "41.300000"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/orders/", 
                               headers=headers, 
                               data=json.dumps(order_data))
        print(f"Status: {response.status_code}")
        
        if response.status_code == 201:
            order = response.json()
            print(f"✅ Yangi format order yaratildi!")
            print(f"Order ID: #{order.get('id', 'N/A')}")
            print(f"Kiruvchi buyumlar: {order.get('kiruvchi_soni', 0)} ta")
            print(f"Chiquvchi buyumlar: {order.get('chiquvchi_soni', 0)} ta")
            return order.get('id')
        else:
            print(f"❌ Order yaratishda xato: {response.text[:300]}")
    
    except Exception as e:
        print(f"❌ Exception: {e}")
    
    return None

def test_orders_list_new_format():
    """Yangi format bilan orders list ko'rish"""
    print("\n📋 Orders list yangi format...")
    
    headers = {"Authorization": f"Token {TOKEN}"}
    
    try:
        response = requests.get(f"{BASE_URL}/orders/", headers=headers)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            orders = data.get('results', [])
            print(f"✅ Jami {len(orders)} ta buyurtma:")
            
            for order in orders[:3]:  # Faqat birinchi 3 tasini ko'rsatish
                kiruvchi = order.get('kiruvchi_soni', 0)
                chiquvchi = order.get('chiquvchi_soni', 0)
                print(f"  #{order.get('id')}: {order.get('full_name')} - K:{kiruvchi}, Ch:{chiquvchi}")
            
            return True
        else:
            print(f"❌ Orders list xato: {response.text[:200]}")
    
    except Exception as e:
        print(f"❌ Exception: {e}")
    
    return False

def test_swagger_docs():
    """Swagger documentation yangilanganligini tekshirish"""
    print("\n📚 Swagger docs testi...")
    
    try:
        response = requests.get("http://127.0.0.1:8000/api/docs/")
        print(f"Swagger status: {response.status_code}")
        
        if response.status_code == 200:
            # Swagger da yangi fieldlar borligini tekshirish
            content = response.text
            if 'kiruvchi_soni' in content and 'chiquvchi_soni' in content:
                print("✅ Swagger da yangi fieldlar mavjud!")
                return True
            else:
                print("⚠️ Swagger da yangi fieldlar ko'rinmayapti")
        else:
            print("❌ Swagger ochilmadi")
    
    except Exception as e:
        print(f"❌ Swagger exception: {e}")
    
    return False

if __name__ == "__main__":
    print("🚀 Yangi buyumlar soni format testini boshlayapman...\n")
    
    # Yangi format bilan order yaratish
    order_id = test_new_order_format()
    
    # Orders list yangi format
    list_ok = test_orders_list_new_format()
    
    # Swagger docs
    swagger_ok = test_swagger_docs()
    
    print(f"\n📊 Natijalar:")
    print(f"Order yaratish: {'✅ OK' if order_id else '❌ FAIL'}")
    print(f"Orders list: {'✅ OK' if list_ok else '❌ FAIL'}")
    print(f"Swagger docs: {'✅ OK' if swagger_ok else '❌ FAIL'}")
    
    if order_id and list_ok:
        print(f"\n🎉 Yangi buyumlar soni format muvaffaqiyatli ishga tushirildi!")
        print(f"🆕 Endi buyurtmalarda direction o'rniga kiruvchi/chiquvchi buyumlar soni bo'ladi")
    else:
        print(f"\n⚠️ Ba'zi testlar muvaffaqiyatsiz, tekshirib ko'ring")