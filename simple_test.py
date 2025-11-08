#!/usr/bin/env python3
import requests
import json
import sys

# API base URL
BASE_URL = "http://127.0.0.1:8000/api"

def test_server_connection():
    """Server bilan bog'lanishni tekshirish"""
    try:
        response = requests.get("http://127.0.0.1:8000/")
        print(f"✅ Server ishlayapti. Status: {response.status_code}")
        return True
    except requests.exceptions.ConnectionError:
        print("❌ Server bilan bog'lanib bo'lmadi!")
        return False

def test_registration():
    """Registratsiya testini o'tkazish"""
    print("\n🔥 Registration test...")
    
    data = {
        "username": "test_user123",
        "password": "securepassword123",
        "password_confirm": "securepassword123",
        "full_name": "Test User",
        "role": "kuryer"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/users/register/", json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 201:
            return response.json().get('token')
        elif response.status_code == 400:
            print("⚠️ Validation xatosi")
            return None
        else:
            print(f"⚠️ Kutilmagan status kod: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Xato: {e}")
        return None

def test_login():
    """Login testini o'tkazish"""
    print("\n🔑 Login test...")
    
    data = {
        "username": "test_user123",
        "password": "securepassword123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/users/login/", json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            return response.json().get('token')
        else:
            print("⚠️ Login muvaffaqiyatsiz")
            return None
            
    except Exception as e:
        print(f"❌ Xato: {e}")
        return None

def test_swagger():
    """Swagger UI ni tekshirish"""
    print("\n📚 Swagger UI test...")
    try:
        response = requests.get("http://127.0.0.1:8000/api/docs/")
        print(f"Swagger UI Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Swagger UI ishlayapti")
        else:
            print("⚠️ Swagger UI bilan muammo")
    except Exception as e:
        print(f"❌ Swagger UI xato: {e}")

if __name__ == "__main__":
    print("🚀 Oddiy API testini boshlayapman...\n")
    
    # Server bilan bog'lanishni tekshirish
    if not test_server_connection():
        sys.exit(1)
    
    # Swagger UI ni tekshirish
    test_swagger()
    
    # Registration test
    token = test_registration()
    
    if not token:
        # Login test
        token = test_login()
    
    if token:
        print(f"\n✅ Token olindi: {token[:30]}...")
        
        # Profile test
        print("\n👤 Profile test...")
        headers = {"Authorization": f"Token {token}"}
        try:
            response = requests.get(f"{BASE_URL}/users/profile/", headers=headers)
            print(f"Profile Status: {response.status_code}")
            print(f"Profile Response: {response.text}")
        except Exception as e:
            print(f"❌ Profile xato: {e}")
    else:
        print("\n❌ Token olib bo'lmadi!")
    
    print("\n🎯 Test yakunlandi!")