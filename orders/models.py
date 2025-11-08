from django.db import models
from django.conf import settings
import random


def generate_order_id():
    """5-xonali random ID generatsiya qilish"""
    return random.randint(10000, 99999)


class Order(models.Model):
    """
    Buyurtma/Client modeli - dastavka buyurtmalari uchun
    """
    
    STATUS_CHOICES = [
        ('kutilmoqda', 'Kutilmoqda'),
        ('bajarildi', 'Bajarildi'),
        ('bekor_qilindi', 'Bekor qilindi'),
    ]
    
    # 5-xonali unique ID
    id = models.PositiveIntegerField(
        primary_key=True, 
        default=generate_order_id,
        verbose_name="Buyurtma ID"
    )
    
    # Mijoz ma'lumotlari
    full_name = models.CharField(
        max_length=255, 
        verbose_name="Ism-familya"
    )
    phone_number = models.CharField(
        max_length=20, 
        verbose_name="Telefon raqam"
    )
    address = models.TextField(
        verbose_name="Manzil"
    )
    
    # Buyumlar soni
    kiruvchi_soni = models.PositiveIntegerField(
        default=0,
        verbose_name="Kiruvchi buyumlar soni"
    )
    chiquvchi_soni = models.PositiveIntegerField(
        default=0,
        verbose_name="Chiquvchi buyumlar soni"
    )
    
    # Qo'shimcha ma'lumotlar
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name="Izoh"
    )
    
    # Geografik koordinatalar
    longitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        blank=True,
        null=True,
        verbose_name="Longitude"
    )
    latitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        blank=True,
        null=True,
        verbose_name="Latitude"
    )
    
    # Status va vaqt
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='kutilmoqda',
        verbose_name="Status"
    )
    
    # Vaqt belgilari
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Yaratilgan sana"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Yangilangan sana"
    )
    
    # Qaysi user yaratgan (ixtiyoriy)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='created_orders',
        verbose_name="Yaratuvchi"
    )
    
    # Qaysi kuryer bajargan (ixtiyoriy)
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='assigned_orders',
        limit_choices_to={'role': 'kuryer'},
        verbose_name="Tayinlangan kuryer"
    )

    class Meta:
        verbose_name = "Buyurtma"
        verbose_name_plural = "Buyurtmalar"
        ordering = ['-created_at']
        
    def save(self, *args, **kwargs):
        # Agar ID allaqachon mavjud bo'lsa, yangi ID generatsiya qilish
        if not self.pk:
            while Order.objects.filter(id=self.id).exists():
                self.id = generate_order_id()
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"#{self.id} - {self.full_name} ({self.status})"
