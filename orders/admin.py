from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'phone_number', 'address', 'status', 'kiruvchi_soni', 'chiquvchi_soni', 'created_by', 'assigned_to', 'created_at')
    list_filter = ('status', 'created_at', 'updated_at', 'created_by', 'assigned_to')
    search_fields = ('id', 'full_name', 'phone_number', 'address', 'notes')
    readonly_fields = ('id', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Buyurtma ma\'lumotlari', {
            'fields': ('id', 'full_name', 'phone_number', 'address', 'kiruvchi_soni', 'chiquvchi_soni', 'notes')
        }),
        ('Manzil koordinatalari', {
            'fields': ('longitude', 'latitude'),
            'classes': ('collapse',),
        }),
        ('Holat va foydalanuvchilar', {
            'fields': ('status', 'created_by', 'assigned_to')
        }),
        ('Vaqt ma\'lumotlari', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        })
    )
