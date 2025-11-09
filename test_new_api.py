"""
Yangi Client model bilan API test qilish
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"
TOKEN = None

def test_login():
    """Login test va token olish"""
    global TOKEN
    print("=== LOGIN TEST ===")
    
    url = f"{BASE_URL}/api/users/login/"
    data = {
        "username": "admin",
        "password": "admin123"
    }
    
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 200:
        TOKEN = response.json()['token']
        print(f"Token: {TOKEN}")
        return True
    return False

def test_create_order():
    """Yangi Client model bilan buyurtma yaratish"""
    print("\n=== CREATE ORDER WITH CLIENT MODEL ===")
    
    url = f"{BASE_URL}/api/orders/"
    headers = {"Authorization": f"Token {TOKEN}"}
    data = {
        "client_full_name": "Test Mijoz",
        "client_phone_number": "+998901234567",
        "client_location_name": "Test Mall",
        "client_address": "Toshkent sh., Chilonzor t., 5-uy",
        "client_longitude": "69.2401",
        "client_latitude": "41.2995",
        "client_notes": "VIP mijoz",
        "kiruvchi_soni": 10,
        "chiquvchi_soni": 5,
        "notes": "Tezkor dastavka kerak"
    }
    
    response = requests.post(url, json=data, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    if response.status_code == 201:
        order_id = response.json()['id']
        print(f"Yaratilgan buyurtma ID: {order_id}")
        return order_id
    return None

def test_get_orders():
    """Buyurtmalar ro'yxatini olish"""
    print("\n=== GET ORDERS LIST ===")
    
    url = f"{BASE_URL}/api/orders/"
    headers = {"Authorization": f"Token {TOKEN}"}
    
    response = requests.get(url, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
def test_get_order_detail(order_id):
    """Buyurtma tafsilotlarini olish"""
    print(f"\n=== GET ORDER DETAIL (ID: {order_id}) ===")
    
    url = f"{BASE_URL}/api/orders/{order_id}/"
    headers = {"Authorization": f"Token {TOKEN}"}
    
    response = requests.get(url, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

def test_update_order(order_id):
    """Buyurtmani yangilash"""
    print(f"\n=== UPDATE ORDER (ID: {order_id}) ===")
    
    url = f"{BASE_URL}/api/orders/{order_id}/"
    headers = {"Authorization": f"Token {TOKEN}"}
    data = {
        "kiruvchi_soni": 15,
        "chiquvchi_soni": 8,
        "notes": "Yangilangan izoh",
        "status": "bajarildi"
    }
    
    response = requests.patch(url, json=data, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

def test_swagger_docs():
    """Swagger dokumentatsiyani test qilish"""
    print("\n=== SWAGGER DOCS TEST ===")
    
    url = f"{BASE_URL}/api/docs/"
    response = requests.get(url)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("Swagger docs ishlamoqda!")
    else:
        print("Swagger docs xatolik!")

def main():
    """Asosiy test funksiyasi"""
    print("🚀 Client Model bilan API Test boshlandi...\n")
    
    # Login test
    if not test_login():
        print("❌ Login muvaffaqiyatsiz! Test to'xtatildi.")
        return
    
    # Buyurtma yaratish
    order_id = test_create_order()
    if not order_id:
        print("❌ Buyurtma yaratilmadi!")
        return
    
    # Buyurtmalar ro'yxati
    test_get_orders()
    
    # Buyurtma tafsilotlari
    test_get_order_detail(order_id)
    
    # Buyurtmani yangilash
    test_update_order(order_id)
    
    # Swagger docs
    test_swagger_docs()
    
    print("\n✅ Barcha testlar tugadi!")

if __name__ == "__main__":
    main()