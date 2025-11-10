#!/usr/bin/env python3
"""
Simple test for basic API endpoints
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def test_basic_endpoints():
    """Test basic endpoints"""
    print("🧪 BASIC API TEST")
    print("="*50)
    
    # Test clients endpoint
    try:
        response = requests.get(f"{BASE_URL}/clients/")
        print(f"📋 Clients endpoint: {response.status_code}")
        if response.status_code == 200:
            clients = response.json()
            print(f"   ✅ Clients count: {len(clients)}")
        else:
            print(f"   ❌ Error: {response.text[:100]}")
    except Exception as e:
        print(f"   ❌ Exception: {e}")
    
    # Test orders endpoint
    try:
        response = requests.get(f"{BASE_URL}/orders/")
        print(f"📦 Orders endpoint: {response.status_code}")
        if response.status_code == 200:
            orders = response.json()
            print(f"   ✅ Orders count: {len(orders)}")
        else:
            print(f"   ❌ Error: {response.text[:100]}")
    except Exception as e:
        print(f"   ❌ Exception: {e}")
    
    # Create a simple client
    client_data = {
        "full_name": "Simple Test Client",
        "phone_number": "+998901234567",
        "address": "Test Address"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/clients/", json=client_data)
        print(f"🆕 Create client: {response.status_code}")
        if response.status_code == 201:
            client = response.json()
            print(f"   ✅ Client created: ID={client['id']}")
            print(f"   ✅ Name: {client['full_name']}")
            print(f"   ✅ Address: {client['address']}")
            # No location_name anymore
            print("   ✅ location_name field removed successfully")
            return client['id']
        else:
            print(f"   ❌ Error: {response.text}")
            return None
    except Exception as e:
        print(f"   ❌ Exception: {e}")
        return None

if __name__ == "__main__":
    test_basic_endpoints()