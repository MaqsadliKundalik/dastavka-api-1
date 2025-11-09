#!/usr/bin/env python3
"""
Server database holatini tekshirish va migration strategiyasini aniqlash
"""

import os
import sys
import django

# Django setup
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dastavka.settings')
django.setup()

from django.db import connection

def check_database_structure():
    """Database jadvallarini tekshirish"""
    cursor = connection.cursor()
    
    print("🔍 DATABASE STRUKTURASINI TEKSHIRISH...")
    print()
    
    # orders_order jadvalini tekshirish
    try:
        cursor.execute("PRAGMA table_info(orders_order)")
        columns = cursor.fetchall()
        
        print("📊 orders_order jadvali ustunlari:")
        existing_columns = []
        for col in columns:
            col_name = col[1]  # column name
            col_type = col[2]  # column type
            existing_columns.append(col_name)
            print(f"  - {col_name}: {col_type}")
        
        print()
        
        # Muhim ustunlarni tekshirish
        required_columns = ['assigned_to_id', 'created_by_id', 'client_id']
        missing_columns = []
        
        for col in required_columns:
            if col in existing_columns:
                print(f"✅ {col} - mavjud")
            else:
                print(f"❌ {col} - yo'q")
                missing_columns.append(col)
        
        print()
        print(f"🎯 Yo'q ustunlar: {missing_columns}")
        
        # orders_client jadvalini tekshirish
        try:
            cursor.execute("PRAGMA table_info(orders_client)")
            client_columns = cursor.fetchall()
            
            if client_columns:
                print("✅ orders_client jadvali mavjud")
                print("📊 orders_client jadvali ustunlari:")
                for col in client_columns:
                    print(f"  - {col[1]}: {col[2]}")
            else:
                print("❌ orders_client jadvali yo'q")
                
        except Exception as e:
            print(f"❌ orders_client jadvalini tekshirishda xatolik: {e}")
            
    except Exception as e:
        print(f"❌ Database tekshirishda xatolik: {e}")

if __name__ == "__main__":
    check_database_structure()