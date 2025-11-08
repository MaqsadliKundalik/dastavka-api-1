#!/usr/bin/env python3
import requests
import json

# API base URL
BASE_URL = "http://127.0.0.1:8000/api"
TOKEN = "0e67507b8fdbe16192d16d81c8ccea6eec889312"

def test_with_token(token):
    """Token bilan API larni test qilish"""
    headers = {"Authorization": f"Token {token}"}
    
    print("🔑 Token bilan testlarni boshlayapman...")
    print(f"Token: {token[:20]}...")
    
    # 1. Profile test
    print("\n👤 Profile test...")
    try:
        response = requests.get(f"{BASE_URL}/users/profile/", headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            user_data = response.json()
            print(f"✅ Profile: {user_data.get('full_name', 'N/A')} ({user_data.get('role', 'N/A')})")
        else:
            print("⚠️ Profile test muvaffaqiyatsiz")
            
    except Exception as e:
        print(f"❌ Profile xato: {e}")
    
    # 2. Users list test
    print("\n📋 Users List test...")
    try:
        response = requests.get(f"{BASE_URL}/users/", headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text[:500]}...")
        
        if response.status_code == 200:
            print("✅ Users list muvaffaqiyatli")
        else:
            print("⚠️ Users list test muvaffaqiyatsiz")
            
    except Exception as e:
        print(f"❌ Users list xato: {e}")
    
    # 3. Orders list test
    print("\n📦 Orders List test...")
    try:
        response = requests.get(f"{BASE_URL}/orders/", headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Orders list muvaffaqiyatli")
        elif response.status_code == 404:
            print("⚠️ Orders endpoint topilmadi")
        else:
            print("⚠️ Orders list test muvaffaqiyatsiz")
            
    except Exception as e:
        print(f"❌ Orders list xato: {e}")
    
    # 4. Create order test
    print("\n📝 Create Order test...")
    try:
        order_data = {
            "full_name": "Ali Valiyev",
            "phone_number": "+998901234567",
            "address": "Toshkent, Yunusobod tumani, 15-uy",
            "direction": "kiruvchi",
            "notes": "Tez yetkazish kerak",
            "longitude": "69.240562",
            "latitude": "41.311081"
        }
        
        response = requests.post(f"{BASE_URL}/orders/", json=order_data, headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 201:
            order_id = response.json().get('id')
            print(f"✅ Order yaratildi: #{order_id}")
            return order_id
        elif response.status_code == 404:
            print("⚠️ Orders create endpoint topilmadi")
        else:
            print("⚠️ Order yaratish muvaffaqiyatsiz")
            
    except Exception as e:
        print(f"❌ Order create xato: {e}")
    
    return None

def test_registration():
    """Yangi user registration"""
    print("\n🔥 Registration test...")
    
    data = {
        "username": "test_user_new",
        "password": "securepass123",
        "password_confirm": "securepass123",
        "full_name": "Test User New",
        "role": "kuryer"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/users/register/", json=data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 201:
            print("✅ Registration muvaffaqiyatli")
            return response.json().get('token')
        else:
            print("⚠️ Registration muvaffaqiyatsiz")
            
    except Exception as e:
        print(f"❌ Registration xato: {e}")
    
    return None

def check_endpoints():
    """Available endpoints ni tekshirish"""
    print("\n🔍 Endpoints ni tekshirish...")
    
    endpoints = [
        "/api/users/",
        "/api/users/register/",
        "/api/users/login/",
        "/api/users/profile/",
        "/api/orders/",
        "/api/docs/",
        "/api/schema/"
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"http://127.0.0.1:8000{endpoint}")
            print(f"{endpoint}: {response.status_code}")
        except Exception as e:
            print(f"{endpoint}: Error - {e}")

if __name__ == "__main__":
    print("🚀 Token bilan API testini boshlayapman...\n")
    
    # Available endpoints check
    check_endpoints()
    
    # Token bilan test
    order_id = test_with_token(TOKEN)
    
    # Registration test
    new_token = test_registration()
    if new_token:
        print(f"\n🎉 Yangi token olindi: {new_token[:20]}...")
    
    print("\n🎯 Test yakunlandi!")