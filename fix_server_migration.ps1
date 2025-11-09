# SERVER MIGRATION MUAMMOSINI HAL QILISH - POWERSHELL VERSIYA

# 1. Migration holatini ko'rish
Write-Host "1️⃣ Migration holatini tekshirish..." -ForegroundColor Yellow
python manage.py showmigrations orders

# 2. Database strukturasini tekshirish
Write-Host "2️⃣ Database strukturasini tekshirish..." -ForegroundColor Yellow
python -c @"
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dastavka.settings')
django.setup()
from django.db import connection
cursor = connection.cursor()
try:
    cursor.execute('PRAGMA table_info(orders_order)')
    columns = cursor.fetchall()
    column_names = [col[1] for col in columns]
    print('Mavjud ustunlar:', column_names)
    print('assigned_to_id mavjud:', 'assigned_to_id' in column_names)
    print('created_by_id mavjud:', 'created_by_id' in column_names)
    print('client_id mavjud:', 'client_id' in column_names)
except Exception as e:
    print('Xatolik:', e)
"@

# 3. Agar duplicate column xatoligi bo'lsa, fake migration qilish
Write-Host "3️⃣ Fake migration qo'llash..." -ForegroundColor Yellow
python manage.py migrate orders --fake

Write-Host "✅ Migration muammosi hal qilinishi kerak!" -ForegroundColor Green