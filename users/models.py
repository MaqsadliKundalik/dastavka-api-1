from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom User modeli dastavka ilovasi uchun
    """
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('kuryer', 'Kuryer'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    
    # AbstractUser da username allaqachon mavjud (login uchun ishlatamiz)
    # Email fieldini o'chiramiz
    email = None
    
    # Email field ni required qilmaslik
    EMAIL_FIELD = None
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    
    full_name = models.CharField(max_length=255, verbose_name="Ism-Familya")
    role = models.CharField(
        max_length=10, 
        choices=ROLE_CHOICES, 
        default='kuryer',
        verbose_name="Rol"
    )
    status = models.CharField(
        max_length=10, 
        choices=STATUS_CHOICES, 
        default='active',
        verbose_name="Status"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan sana")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan sana")
    
    class Meta:
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"
        
    def __str__(self):
        return f"{self.username} - {self.full_name}"
