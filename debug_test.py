#!/usr/bin/env python3
import requests
import json

TOKEN = "0e67507b8fdbe16192d16d81c8ccea6eec889312"
BASE_URL = "http://127.0.0.1:8000/api"

def simple_profile_test():
    """Faqat profile endpoint ni test qilish"""
    print("🔍 Profile endpoint test...")
    
    headers = {"Authorization": f"Token {TOKEN}"}
    
    try:
        # Profile endpoint
        response = requests.get(f"{BASE_URL}/users/profile/", headers=headers)
        print(f"Profile Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Profile ishlayapti!")
            print(f"User: {data.get('full_name', 'N/A')} ({data.get('role', 'N/A')})")
            return True
        else:
            print(f"❌ Profile error: {response.text[:200]}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Server bilan bog'lanish muammosi")
        return False
    except Exception as e:
        print(f"❌ Noma'lum xato: {e}")
        return False

def simple_registration_test():
    """Oddiy registration test"""
    print("\n🔍 Registration endpoint test...")
    
    # Super oddiy ma'lumotlar
    data = {
        "username": "testuser123",
        "password": "password123",
        "password_confirm": "password123",
        "full_name": "Test User",
        "role": "kuryer"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/users/register/", json=data)
        print(f"Registration Status: {response.status_code}")
        
        if response.status_code == 201:
            print("✅ Registration ishlayapti!")
            result = response.json()
            print(f"Token: {result.get('token', 'N/A')[:20]}...")
            return True
        else:
            print(f"❌ Registration error: {response.text[:300]}")
            return False
            
    except Exception as e:
        print(f"❌ Registration xato: {e}")
        return False

def check_api_availability():
    """API mavjudligini tekshirish"""
    print("🔍 API endpoints mavjudligini tekshirish...")
    
    endpoints = [
        "/api/users/profile/",
        "/api/users/register/",
        "/api/users/login/",
        "/api/users/",
        "/api/orders/",
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"http://127.0.0.1:8000{endpoint}")
            print(f"{endpoint}: {response.status_code}")
        except Exception as e:
            print(f"{endpoint}: Error - {str(e)[:50]}")

if __name__ == "__main__":
    print("🚀 API diagnostika testini boshlayapman...\n")
    
    # API endpoints mavjudligini tekshirish
    check_api_availability()
    
    # Profile test (token bilan)
    profile_ok = simple_profile_test()
    
    # Registration test (token siz)
    reg_ok = simple_registration_test()
    
    print(f"\n📊 Natijalar:")
    print(f"Profile test: {'✅ OK' if profile_ok else '❌ FAIL'}")
    print(f"Registration test: {'✅ OK' if reg_ok else '❌ FAIL'}")
    
    if not profile_ok and not reg_ok:
        print("\n🚨 Barcha testlar muvaffaqiyatsiz!")
        print("Serverni qayta ishga tushiring yoki debug qiling.")
    else:
        print("\n🎉 Ba'zi testlar muvaffaqiyatli!")