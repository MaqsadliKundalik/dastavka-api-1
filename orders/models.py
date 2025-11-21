from django.db import models
from django.conf import settings
import random


class Client(models.Model):
    """
    Mijoz (Buyurtmachi) modeli - mijozlar ma'lumotlari uchun
    """
    
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
        verbose_name="To'liq manzil"
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
    
    # Qo'shimcha ma'lumotlar
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name="Mijoz haqida izoh"
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

    class Meta:
        verbose_name = "Mijoz"
        verbose_name_plural = "Mijozlar"
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.full_name} - {self.phone_number}"
        
    @property
    def orders_count(self):
        """Mijozning buyurtmalari soni"""
        return self.orders.count()


class Order(models.Model):
    """
    Buyurtma modeli
    """
    
    STATUS_CHOICES = [
        ('kútilmekte', 'kútilmekte'),
        ('orınlandı', 'orınlandı'),
        ('bekor_qilindi', 'Bekor qilindi'),
    ]
    
    @staticmethod
    def generate_unique_order_id():
        """
        Unique ID generatsiya qilish:
        - 5 xonali ID-lar (10000-99999) bilan boshlanadi
        - Agar 5 xonali ID-lar tugasa, 6 xonali ID-larga (100000-999999) o'tadi
        - Va hokazo...
        """
        
        # ID intervallarini aniqlash
        ranges = [
            (10000, 99999),      # 5 xonali
            (100000, 999999),    # 6 xonali  
            (1000000, 9999999),  # 7 xonali
            (10000000, 99999999) # 8 xonali
        ]
        
        max_attempts = 50  # Har bir range uchun maksimal urinishlar
        
        for min_id, max_id in ranges:
            # Har bir range-da random ID qidirish
            for attempt in range(max_attempts):
                order_id = random.randint(min_id, max_id)
                
                # Agar bu ID mavjud bo'lmasa, qaytarish
                if not Order.objects.filter(id=order_id).exists():
                    return order_id
            
            # Agar random ID topilmasa, sequential ravishda qidirish
            existing_ids_in_range = set(
                Order.objects.filter(
                    id__gte=min_id, 
                    id__lte=max_id
                ).values_list('id', flat=True)
            )
            
            # Range ichida bo'sh ID qidirish
            for potential_id in range(min_id, max_id + 1):
                if potential_id not in existing_ids_in_range:
                    return potential_id
        
        # Agar barcha range-lar to'lsa, eng katta ID + 1 qaytarish
        last_order = Order.objects.order_by('-id').first()
        if last_order:
            return last_order.id + 1
        
        return 10000  # Default birinchi ID
    
    # 5-xonali unique ID
    id = models.PositiveIntegerField(
        primary_key=True, 
        verbose_name="Buyurtma ID"
    )
    
    # Mijoz (Foreign Key)
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name="Mijoz"
    )
    
    # Zakazlar soni
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
    
    # Buyurtma haqida qo'shimcha ma'lumotlar
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name="Buyurtma haqida izoh"
    )
    
    # Status va vaqt
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='kútilmekte',
        verbose_name="Status"
    )
    
    # Vaqt belgilari
    created_at = models.DateField(
        auto_now_add=True,
        verbose_name="Yaratilgan sana (sana)"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Yangilangan sana"
    )

    # Buyurtma narxi
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Buyurtma narxi (so'm)",
        default=0
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
            self.id = self.generate_unique_order_id()
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"#{self.id} - {self.client.full_name if self.client else 'No Client'} ({self.status})"
