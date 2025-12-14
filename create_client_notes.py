"""
Mavjud barcha clientlar uchun avtomatik ClientNotes obyektlarini yaratish scripti
"""
import os
import django

# Django sozlamalarini yuklash
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dastavka.settings')
django.setup()

from orders.models import Client, ClientNotes

def create_notes_for_clients():
    """
    Barcha mavjud clientlar uchun ClientNotes yaratish
    """
    # Barcha clientlarni olish
    clients = Client.objects.all()
    total_clients = clients.count()
    
    print(f"Jami {total_clients} ta client topildi.")
    print("ClientNotes yaratish boshlandi...\n")
    
    created_count = 0
    already_exists_count = 0
    
    for client in clients:
        # Bu client uchun notes mavjudmi tekshirish
        if ClientNotes.objects.filter(client=client).exists():
            print(f"❌ Client #{client.id} ({client.full_name}) uchun notes allaqachon mavjud")
            already_exists_count += 1
        else:
            # Yangi notes yaratish
            ClientNotes.objects.create(
                client=client,
                baklashka_soni=0,
                arenda_soni=0,
                kuler_soni=0,
                pompa_soni=0
            )
            print(f"✅ Client #{client.id} ({client.full_name}) uchun notes yaratildi")
            created_count += 1
    
    print(f"\n{'='*60}")
    print(f"Natija:")
    print(f"  - Yangi yaratilgan notes: {created_count}")
    print(f"  - Allaqachon mavjud: {already_exists_count}")
    print(f"  - Jami: {total_clients}")
    print(f"{'='*60}")

if __name__ == '__main__':
    create_notes_for_clients()
