#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def test_users_endpoints():
    print("🎯 USERS ENDPOINT-LARINI AVTORIZATSIYASIZ TESTLASH!")
    print("🚀 USERS API TESTLARI")
    print("=" * 60)
    
    # 1. Userlar ro'yxatini olish
    print("\n1. Barcha userlar ro'yxati:")
    try:
        response = requests.get(f"{BASE_URL}/users/")
        print(f"   📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            users = response.json()
            print(f"   ✅ MUVAFFAQIYAT! Jami userlar: {len(users)}")
            if users:
                first_three = users[:3] if len(users) > 3 else users
                for i, user in enumerate(first_three, 1):  # Faqat birinchi 3 ta
                    print(f"   {i}. ID: {user.get('id')} - {user.get('username')} ({user.get('full_name')})")
        else:
            print(f"   ❌ XATOLIK: {response.text}")
    except Exception as e:
        print(f"   ⚠️ CONNECTION ERROR: {e}")
    
    # 2. Bitta user ma'lumotlarini olish (ID=1)
    print("\n2. ID=1 bo'lgan user ma'lumotlari:")
    try:
        response = requests.get(f"{BASE_URL}/users/1/")
        print(f"   📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            user = response.json()
            print(f"   ✅ MUVAFFAQIYAT!")
            print(f"      🆔 ID: {user.get('id')}")
            print(f"      👤 Username: {user.get('username')}")
            print(f"      📝 Full Name: {user.get('full_name')}")
            print(f"      🔧 Role: {user.get('role')}")
            print(f"      ✅ Status: {user.get('status')}")
        else:
            print(f"   ❌ XATOLIK: {response.text}")
    except Exception as e:
        print(f"   ⚠️ CONNECTION ERROR: {e}")
    
    # 3. User registration test
    print("\n3. Yangi user ro'yxatdan o'tkazish:")
    try:
        new_user_data = {
            "username": "test_user_temp",
            "password": "testpass123",
            "full_name": "Test User Temp",
            "role": "kuryer"
        }
        
        print(f"   📤 Yuborilayotgan ma'lumotlar:")
        print(f"   {json.dumps(new_user_data, indent=6, ensure_ascii=False)}")
        
        response = requests.post(f"{BASE_URL}/users/register/", json=new_user_data)
        print(f"   📊 Status: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()
            print(f"   ✅ MUVAFFAQIYAT! Yangi user yaratildi:")
            print(f"      🆔 User ID: {result.get('user', {}).get('id')}")
            print(f"      👤 Username: {result.get('user', {}).get('username')}")
            print(f"      🔑 Token: {result.get('token')[:20]}...")
            print(f"      💬 Message: {result.get('message')}")
        else:
            print(f"   ❌ XATOLIK: {response.text}")
    except Exception as e:
        print(f"   ⚠️ CONNECTION ERROR: {e}")
    
    # 4. User login test  
    print("\n4. User login testi:")
    try:
        login_data = {
            "username": "test_user_temp",
            "password": "testpass123"
        }
        
        print(f"   📤 Login ma'lumotlari:")
        print(f"   {json.dumps(login_data, indent=6, ensure_ascii=False)}")
        
        response = requests.post(f"{BASE_URL}/users/login/", json=login_data)
        print(f"   📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ MUVAFFAQIYAT! Login amalga oshirildi:")
            print(f"      👤 Username: {result.get('user', {}).get('username')}")
            print(f"      🔑 Token: {result.get('token')[:20]}...")
            print(f"      💬 Message: {result.get('message')}")
        else:
            print(f"   ❌ XATOLIK: {response.text}")
    except Exception as e:
        print(f"   ⚠️ CONNECTION ERROR: {e}")

    print("\n" + "=" * 60)
    print("🎉 USERS TESTLARI YAKUNLANDI!")
    
    print("\n📋 XULOSA:")
    print("✅ USERS ENDPOINT-LARI:")
    print("   - GET /api/users/ - Barcha userlar")
    print("   - GET /api/users/{id}/ - Bitta user")
    print("   - POST /api/users/register/ - Ro'yxatdan o'tish")
    print("   - POST /api/users/login/ - Tizimga kirish")

if __name__ == "__main__":
    test_users_endpoints()