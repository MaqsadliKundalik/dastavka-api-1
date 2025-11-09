#!/bin/bash

# SERVER MIGRATION MUAMMOSINI HAL QILISH

echo "🔧 Server migration muammosini bartaraf etish..."

# 1. Migration holatini tekshirish
echo "1️⃣ Migration holatini ko'rish:"
python manage.py showmigrations orders

# 2. Muammoli migrationni fake qilish
echo "2️⃣ Muammoli migrationni fake qilish:"
python manage.py migrate orders 0001 --fake

# 3. Database strukturasini tekshirish
echo "3️⃣ Database strukturasini tekshirish:"
python -c "
import django
django.setup()
from django.db import connection
cursor = connection.cursor()
cursor.execute('PRAGMA table_info(orders_order)')
columns = cursor.fetchall()
print('Mavjud ustunlar:')
for col in columns:
    print(f'  - {col[1]}: {col[2]}')
"

# 4. Agar assigned_to_id mavjud bo'lsa, migration faylni o'zgartirish
echo "4️⃣ Conditional migration qo'llash:"

# Database-da assigned_to_id mavjudligini tekshirish
ASSIGNED_TO_EXISTS=$(python -c "
import django
django.setup()
from django.db import connection
cursor = connection.cursor()
cursor.execute('PRAGMA table_info(orders_order)')
columns = [row[1] for row in cursor.fetchall()]
print('assigned_to_id' in columns)
")

if [ "$ASSIGNED_TO_EXISTS" = "True" ]; then
    echo "✅ assigned_to_id allaqachon mavjud, migration o'tkazib yuboriladi"
    python manage.py migrate orders --fake
else
    echo "❌ assigned_to_id yo'q, migration qo'llanadi"
    python manage.py migrate orders
fi

echo "✅ Migration muammosi hal qilindi!"