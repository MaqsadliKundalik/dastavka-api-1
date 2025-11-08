#!/usr/bin/env python3
import requests
import json

TOKEN = "0e67507b8fdbe16192d16d81c8ccea6eec889312"
BASE_URL = "http://127.0.0.1:8000/api"

def test_registration_with_different_methods():
    """Turli xil metodlar bilan registration test"""
    print("🔍 Registration test - turli metodlar...")
    
    data = {
        "username": "newuser123",
        "password": "password123",
        "password_confirm": "password123",
        "full_name": "New User",
        "role": "kuryer"
    }
    
    # Method 1: JSON data
    print("\n1️⃣ JSON Content-Type bilan:")
    try:
        headers = {'Content-Type': 'application/json'}
        response = requests.post(f"{BASE_URL}/users/register/", 
                               headers=headers, 
                               data=json.dumps(data))
        print(f"Status: {response.status_code}")
        if response.status_code == 201:
            print("✅ JSON method muvaffaqiyatli!")
            result = response.json()
            print(f"Token: {result.get('token', 'N/A')[:20]}...")
            return True
        else:
            print(f"❌ JSON method error: {response.text[:200]}")
    except Exception as e:
        print(f"❌ JSON method exception: {e}")
    
    # Method 2: Form data
    print("\n2️⃣ Form data bilan:")
    try:
        response = requests.post(f"{BASE_URL}/users/register/", data=data)
        print(f"Status: {response.status_code}")
        if response.status_code == 201:
            print("✅ Form method muvaffaqiyatli!")
            result = response.json()
            print(f"Token: {result.get('token', 'N/A')[:20]}...")
            return True
        else:
            print(f"❌ Form method error: {response.text[:200]}")
    except Exception as e:
        print(f"❌ Form method exception: {e}")
    
    return False

def test_orders_with_token():
    """Orders API ni token bilan test qilish"""
    print("\n🔍 Orders API test...")
    
    headers = {"Authorization": f"Token {TOKEN}"}
    
    # Orders list
    try:
        response = requests.get(f"{BASE_URL}/orders/", headers=headers)
        print(f"Orders list status: {response.status_code}")
        
        if response.status_code == 200:
            orders = response.json()
            print(f"✅ Orders list ishlayapti! Jami: {len(orders.get('results', orders))} ta buyurtma")
            return True
        else:
            print(f"❌ Orders list failed: {response.text[:200]}")
    
    except Exception as e:
        print(f"❌ Orders exception: {e}")
    
    return False

def test_create_order():
    """Buyurtma yaratish test"""
    print("\n🔍 Order yaratish test...")
    
    headers = {
        "Authorization": f"Token {TOKEN}",
        "Content-Type": "application/json"
    }
    
    order_data = {
        "full_name": "Test Mijoz",
        "phone_number": "+998901234567",
        "address": "Toshkent, Test Address",
        "direction": "kiruvchi",
        "notes": "Test buyurtma"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/orders/", 
                               headers=headers, 
                               data=json.dumps(order_data))
        print(f"Create order status: {response.status_code}")
        
        if response.status_code == 201:
            order = response.json()
            print(f"✅ Order yaratildi! ID: {order.get('id', 'N/A')}")
            return order.get('id')
        else:
            print(f"❌ Order yaratish failed: {response.text[:300]}")
    
    except Exception as e:
        print(f"❌ Order create exception: {e}")
    
    return None

if __name__ == "__main__":
    print("🚀 Kengaytirilgan API testini boshlayapman...\n")
    
    # Registration test
    reg_success = test_registration_with_different_methods()
    
    # Orders test
    orders_success = test_orders_with_token()
    
    # Create order test  
    order_id = test_create_order()
    
    print(f"\n📊 Yakuniy natijalar:")
    print(f"Registration: {'✅ OK' if reg_success else '❌ FAIL'}")
    print(f"Orders list: {'✅ OK' if orders_success else '❌ FAIL'}")
    print(f"Create order: {'✅ OK' if order_id else '❌ FAIL'}")
    
    if orders_success:
        print("\n🎉 Orders API ishlayapti!")
    if order_id:
        print(f"🎉 Yangi buyurtma yaratildi: #{order_id}")