#!/usr/bin/env python
"""
Client ID bo'yicha filterlashni test qilish
"""

import requests
import json

# Base URL
BASE_URL = "http://localhost:8000/api"

def get_auth_token():
    """Login qilish va token olish"""
    login_data = {
        "username": "testadmin",
        "password": "admin123"
    }
    
    response = requests.post(f"{BASE_URL}/users/login/", json=login_data)
    if response.status_code == 200:
        token = response.json()['token']
        print(f"✅ Login muvaffaqiyatli! Token: {token[:20]}...")
        return token
    else:
        print(f"❌ Login xatosi: {response.status_code}")
        print(f"Response: {response.text}")
        return None

def test_client_id_filter(token):
    """Client ID filterlashni test qilish"""
    headers = {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json"
    }
    
    print("\n🔍 CLIENT ID FILTERLASH TESTLARI:")
    
    # 1. Avval barcha buyurtmalarni ko'ramiz
    print("\n1. Barcha buyurtmalar:")
    response = requests.get(f"{BASE_URL}/orders/", headers=headers)
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Jami buyurtmalar: {data['count']}")
        
        # Avval to'liq order ma'lumotlarini olamiz (OrderSerializer bilan)
        response_detail = requests.get(f"{BASE_URL}/orders/{data['results'][0]['id']}/", headers=headers)
        if response_detail.status_code == 200:
            order_detail = response_detail.json()
            if 'client' in order_detail:
                print("   📋 Mavjud Client ID'lar:")
                client_ids = []
                
                # Birinchi buyurtmaning client ID sini olamiz
                client_id = order_detail['client']['id']
                client_ids.append(client_id)
                print(f"      - Buyurtma {order_detail['id']}: Client ID {client_id} ({order_detail['client']['full_name']})")
                
                # Boshqa buyurtmalarni ham tekshiramiz
                for order in data['results'][1:3]:  # Keyingi 2 tasini
                    resp = requests.get(f"{BASE_URL}/orders/{order['id']}/", headers=headers)
                    if resp.status_code == 200:
                        order_data = resp.json()
                        if 'client' in order_data:
                            client_id = order_data['client']['id']
                            client_ids.append(client_id)
                            print(f"      - Buyurtma {order_data['id']}: Client ID {client_id} ({order_data['client']['full_name']})")
                
                # Test uchun birinchi client ID ni olamiz
                if client_ids:
                    test_client_id = str(client_ids[0])
                
                    print(f"\n2. Client ID {test_client_id} bo'yicha to'liq qidirish:")
                    response = requests.get(f"{BASE_URL}/orders/?client_id={test_client_id}", headers=headers)
                    if response.status_code == 200:
                        data = response.json()
                        print(f"   ✅ Client ID {test_client_id} uchun {data['count']} ta buyurtma topildi")
                        for order in data['results']:
                            print(f"      - Buyurtma {order['id']}: {order['client_full_name']}")
                    
                    # Partial qidirish (ID ning bir qismini kiritish)
                    if len(test_client_id) >= 2:
                        partial_id = test_client_id[:2]  # ID ning birinchi 2 ta raqami
                        print(f"\n3. Client ID da '{partial_id}' qismi bo'yicha qidirish:")
                        response = requests.get(f"{BASE_URL}/orders/?client_id={partial_id}", headers=headers)
                        if response.status_code == 200:
                            data = response.json()
                            print(f"   ✅ ID'sida '{partial_id}' bo'lgan clientlar uchun {data['count']} ta buyurtma topildi")
                            for order in data['results'][:3]:  # Faqat birinchi 3 tasini ko'rsatamiz
                                # Her bir buyurtma uchun to'liq ma'lumot olamiz
                                resp = requests.get(f"{BASE_URL}/orders/{order['id']}/", headers=headers)
                                if resp.status_code == 200:
                                    order_detail = resp.json()
                                    if 'client' in order_detail:
                                        print(f"      - Buyurtma {order['id']}: Client ID {order_detail['client']['id']} ({order_detail['client']['full_name']})")
                    
                    # Boshqa test - oxirgi raqamlar bo'yicha
                    if len(test_client_id) >= 3:
                        last_digits = test_client_id[-2:]  # ID ning oxirgi 2 ta raqami
                        print(f"\n4. Client ID oxirida '{last_digits}' bo'yicha qidirish:")
                        response = requests.get(f"{BASE_URL}/orders/?client_id={last_digits}", headers=headers)
                        if response.status_code == 200:
                            data = response.json()
                            print(f"   ✅ ID'si '{last_digits}' bilan tugaydigan clientlar uchun {data['count']} ta buyurtma topildi")
    
    # Client nomi bo'yicha ham test qilamiz
    print("\n5. Client nomi bo'yicha qidirish:")
    response = requests.get(f"{BASE_URL}/orders/?client_name=a", headers=headers)
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Nomida 'a' harfi bo'lgan clientlar uchun {data['count']} ta buyurtma topildi")
    
    # Telefon raqam bo'yicha test
    print("\n6. Client telefon raqami bo'yicha qidirish:")
    response = requests.get(f"{BASE_URL}/orders/?client_phone=998", headers=headers)
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Telefon raqamida '998' bo'lgan clientlar uchun {data['count']} ta buyurtma topildi")

def main():
    print("🚀 CLIENT ID FILTERLASH TESTLARI BOSHLANDI!")
    print("=" * 60)
    
    # Token olish
    token = get_auth_token()
    if not token:
        print("❌ Token olishda xatolik!")
        return
    
    # Client ID filterlashni test qilish
    test_client_id_filter(token)
    
    print("\n" + "=" * 60)
    print("🎉 CLIENT ID FILTERLASH TESTLARI YAKUNLANDI!")
    
    print("\n📋 QO'LLANILISHI MUMKIN BO'LGAN FILTERLAR:")
    print("   ?client_id=123        - Client ID to'liq yoki qismiy qidirish")
    print("   ?client_name=ahmad    - Client nomi bo'yicha qidirish")
    print("   ?client_phone=998     - Client telefon raqami bo'yicha qidirish")
    print("   ?status=kutilmoqda    - Buyurtma statusi bo'yicha")
    
    print("\n💡 MISOLLAR:")
    print("   /api/orders/?client_id=12     - ID'sida '12' bo'lgan barcha clientlar")
    print("   /api/orders/?client_id=345    - ID'sida '345' bo'lgan barcha clientlar")
    print("   /api/orders/?client_id=1&client_name=ahmad  - Kombinatsiya")

if __name__ == "__main__":
    main()