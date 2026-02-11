from django.db import models


class Client(models.Model):
    """
    Mijoz (Buyurtmachi) modeli - mijozlar ma'lumotlari uchun
    """
    
    full_name = models.CharField(
        max_length=255, 
        verbose_name="Ism-familya"
    )
    phone_number = models.CharField(
        max_length=20, 
        verbose_name="Telefon raqam"
    )
    
    location_name = models.CharField(
        max_length=255,
        verbose_name="Manzil nomi/Tavsifi"
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
        """Mijozning buyurtmalari soni"""
        return self.orders.count()