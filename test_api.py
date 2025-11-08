import requests
import json

# API base URL
BASE_URL = "http://127.0.0.1:8000/api"

def test_user_registration():
    """
    User registration testini o'tkazish
    """
    print("🔥 User Registration testini boshlayapman...")
    
    data = {
        "username": "test_kuryer",
        "password": "secure123456",
        "password_confirm": "secure123456", 
        "full_name": "Jasur Karimov",
        "role": "kuryer"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/users/register/", json=data)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code in [200, 201]:
            response_data = response.json()
            print(f"Response: {json.dumps(response_data, indent=2, ensure_ascii=False)}")
            return response_data.get('token')
        else:
            print(f"Response Text: {response.text}")
            return None
            
    except requests.exceptions.JSONDecodeError:
        print(f"JSON decode error. Response text: {response.text}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def test_user_login():
    """
    User login testini o'tkazish
    """
    print("\n🔑 User Login testini boshlayapman...")
    
    data = {
        "username": "test_kuryer",
        "password": "secure123456"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/users/login/", json=data)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code in [200, 201]:
            response_data = response.json()
            print(f"Response: {json.dumps(response_data, indent=2, ensure_ascii=False)}")
            return response_data.get('token')
        else:
            print(f"Response Text: {response.text}")
            return None
            
    except requests.exceptions.JSONDecodeError:
        print(f"JSON decode error. Response text: {response.text}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def test_user_profile(token):
    """
    User profile testini o'tkazish
    """
    print("\n👤 User Profile testini boshlayapman...")
    
    headers = {
        "Authorization": f"Token {token}"
    }
    
    response = requests.get(f"{BASE_URL}/users/profile/", headers=headers)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

def test_update_profile(token):
    """
    Profile update testini o'tkazish
    """
    print("\n✏️ Profile Update testini boshlayapman...")
    
    headers = {
        "Authorization": f"Token {token}"
    }
    
    data = {
        "full_name": "Jasur Karimov (Yangilandi)"
    }
    
    response = requests.put(f"{BASE_URL}/users/profile/", json=data, headers=headers)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

def test_users_list(token):
    """
    Users list testini o'tkazish
    """
    print("\n📋 Users List testini boshlayapman...")
    
    headers = {
        "Authorization": f"Token {token}"
    }
    
    response = requests.get(f"{BASE_URL}/users/", headers=headers)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

def test_user_logout(token):
    """
    User logout testini o'tkazish
    """
    print("\n🚪 User Logout testini boshlayapman...")
    
    headers = {
        "Authorization": f"Token {token}"
    }
    
    response = requests.post(f"{BASE_URL}/users/logout/", headers=headers)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

def test_create_order(token):
    """
    Buyurtma yaratish testini o'tkazish
    """
    print("\n📦 Order Create testini boshlayapman...")
    
    headers = {
        "Authorization": f"Token {token}"
    }
    
    data = {
        "full_name": "Ali Valijonov", 
        "phone_number": "+998901234567",
        "address": "Toshkent, Chilonzor tumani, 5-uy",
        "kiruvchi_soni": 5,
        "chiquvchi_soni": 2,
        "notes": "Tez yetkazish kerak, 3-qavat",
        "longitude": "69.240562",
        "latitude": "41.311081"
    }
    
    response = requests.post(f"{BASE_URL}/orders/", json=data, headers=headers)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    if response.status_code == 201:
        return response.json()['id']
    return None

def test_orders_list(token):
    """
    Buyurtmalar ro'yxatini olish testini o'tkazish
    """
    print("\n📋 Orders List testini boshlayapman...")
    
    headers = {
        "Authorization": f"Token {token}"
    }
    
    response = requests.get(f"{BASE_URL}/orders/", headers=headers)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

def test_my_orders(token):
    """
    Mening buyurtmalarim testini o'tkazish
    """
    print("\n👤 My Orders testini boshlayapman...")
    
    headers = {
        "Authorization": f"Token {token}"
    }
    
    response = requests.get(f"{BASE_URL}/orders/my/", headers=headers)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

def test_order_detail(token, order_id):
    """
    Buyurtma tafsilotlarini olish testini o'tkazish
    """
    if not order_id:
        print("\n⚠️ Order Detail test o'tkazib yuborildi (Order ID yo'q)")
        return
        
    print(f"\n🔍 Order Detail testini boshlayapman (ID: {order_id})...")
    
    headers = {
        "Authorization": f"Token {token}"
    }
    
    response = requests.get(f"{BASE_URL}/orders/{order_id}/", headers=headers)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

def test_update_order_status(token, order_id):
    """
    Buyurtma statusini yangilash testini o'tkazish
    """
    if not order_id:
        print("\n⚠️ Update Status test o'tkazib yuborildi (Order ID yo'q)")
        return
        
    print(f"\n✏️ Update Order Status testini boshlayapman (ID: {order_id})...")
    
    headers = {
        "Authorization": f"Token {token}"
    }
    
    data = {
        "status": "bajarildi"
    }
    
    response = requests.patch(f"{BASE_URL}/orders/{order_id}/status/", json=data, headers=headers)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

if __name__ == "__main__":
    print("🚀 Django REST API Testlarini boshlayapman...\n")
    
    try:
        # User registration
        token = test_user_registration()
        
        if not token:
            # Agar registration muvaffaqiyatsiz bo'lsa, login qilib ko'ramiz
            print("\n🔄 Registration muvaffaqiyatsiz, Login qilib ko'raman...")
            token = test_user_login()
        
        if token:
            print(f"\n✅ Token olindi: {token[:20]}...")
            
            # ==== USER API TESTLARI ====
            print("\n" + "="*50)
            print("🔵 USER API TESTLARI")
            print("="*50)
            
            # User profile
            test_user_profile(token)
            
            # Update profile
            test_update_profile(token)
            
            # Users list
            test_users_list(token)
            
            # ==== ORDERS API TESTLARI ====
            print("\n" + "="*50)
            print("🟢 ORDERS API TESTLARI")
            print("="*50)
            
            # Create order
            order_id = test_create_order(token)
            
            # Orders list
            test_orders_list(token)
            
            # My orders
            test_my_orders(token)
            
            # Order detail
            test_order_detail(token, order_id)
            
            # Update order status
            test_update_order_status(token, order_id)
            
            # User logout
            print("\n" + "="*50)
            print("🔴 LOGOUT TEST")
            print("="*50)
            test_user_logout(token)
            
            print("\n🎉 Barcha testlar muvaffaqiyatli yakunlandi!")
            
        else:
            print("\n❌ Token olib bo'lmadi! Server ishlayotganini tekshiring.")
            
    except requests.exceptions.ConnectionError:
        print("❌ Server bilan bog'lanib bo'lmadi!")
        print("Avval serverni ishga tushiring: python manage.py runserver")
    except Exception as e:
        print(f"❌ Test xatosi: {e}")