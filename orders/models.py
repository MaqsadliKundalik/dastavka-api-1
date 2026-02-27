from django.db import models
from django.conf import settings
import random


class Client(models.Model):
    full_name = models.CharField(
        max_length=255, 
        verbose_name="Ism-familya"
    )
    phone_number = models.CharField(
        max_length=20, 
        verbose_name="Telefon raqam"
    )
    
    address = models.TextField(
        verbose_name="To'liq manzil"
    )
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
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name="Mijoz haqida izoh"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Yaratilgan sana"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Yangilangan sana"
    )

    class Meta:
        verbose_name = "Mijoz"
        verbose_name_plural = "Mijozlar"
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.full_name} - {self.phone_number}"
        
    @property
    def orders_count(self):
        return self.orders.count()

class ClientNotes(models.Model):
    client = models.OneToOneField(
        Client,
        on_delete=models.CASCADE,
        unique=True,
        related_name='client_notes'
    )
    baklashka_soni = models.PositiveIntegerField(
        default=0,
        verbose_name="Baklashkalar soni"
    )   
    arenda_soni = models.PositiveIntegerField(
        default=0,  
        verbose_name="Arenda soni"
    )
    kuler_soni = models.PositiveIntegerField(
        default=0,
        verbose_name="Kulerlar soni"
    )
    pompa_soni = models.PositiveIntegerField(
        default=0,
        verbose_name="Pompalar soni"
    )

    class Meta:
        verbose_name = "Client Notes"
        verbose_name_plural = "Client Notes"

    def __str__(self):
        return f"Notes for {self.client.full_name}"

class Order(models.Model):
    STATUS_CHOICES = [
        ('kutilmoqda', 'Kutilmoqda'),
        ('kuryerga_berildi', 'Kuryerga berildi'),
        ('yolda', 'Yo\'lda'),
        ('yetkazildi', 'Yetkazildi'),
        ('bajarildi', 'Bajarildi'),
        ('bekor_qilindi', 'Bekor qilindi'),
    ]
    
    @staticmethod
    def generate_unique_order_id():
        ranges = [
            (10000, 99999),      # 5 xonali
            (100000, 999999),    # 6 xonali  
            (1000000, 9999999),  # 7 xonali
            (10000000, 99999999) # 8 xonali
        ]
        max_attempts = 50
        
        for min_id, max_id in ranges:
            for attempt in range(max_attempts):
                order_id = random.randint(min_id, max_id)
                if not Order.objects.filter(id=order_id).exists():
                    return order_id
            
            existing_ids_in_range = set(
                Order.objects.filter(
                    id__gte=min_id, 
                    id__lte=max_id
                ).values_list('id', flat=True)
            )
            for potential_id in range(min_id, max_id + 1):
                if potential_id not in existing_ids_in_range:
                    return potential_id
        
        last_order = Order.objects.order_by('-id').first()
        if last_order:
            return last_order.id + 1
        return 10000
    
    id = models.PositiveIntegerField(
        primary_key=True, 
        verbose_name="Buyurtma ID"
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name="Mijoz"
    )
    baklashka_soni = models.PositiveIntegerField(
        default=0,
        verbose_name="Baklashkalar soni"
    )
    arenda_soni = models.PositiveIntegerField(
        default=0,
        verbose_name="Arenda soni"
    )
    baklashkasiz_soni = models.PositiveIntegerField(
        default=0,
        verbose_name="Baklashkasiz soni"
    )
    kuler_soni = models.PositiveIntegerField(
        default=0,
        verbose_name="Kulerlar soni"
    )
    pompa_soni = models.PositiveIntegerField(
        default=0,
        verbose_name="Pompalar soni"
    )
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name="Buyurtma haqida izoh"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='kutilmoqda',
        verbose_name="Status"
    )
    created_at = models.DateField(
        auto_now_add=True,
        verbose_name="Yaratilgan sana (sana)"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Yangilangan sana"
    )
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Buyurtma narxi (so'm)",
        default=0
    )
    is_debit = models.BooleanField(
        verbose_name="Qarz",
        default=False
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='created_orders',
        verbose_name="Yaratuvchi"
    )
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
        if not self.pk:
            self.id = self.generate_unique_order_id()
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"#{self.id} - {self.client.full_name if self.client else 'No Client'} ({self.status})"
