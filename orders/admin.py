from django.contrib import admin
from .models import Order, Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'phone_number', 'created_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('full_name', 'phone_number', 'address')
    readonly_fields = ('id', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Mijoz ma\'lumotlari', {
            'fields': ('id', 'full_name', 'phone_number')
        }),
        ('Manzil ma\'lumotlari', {
            'fields': ('address', 'longitude', 'latitude')
        }),
        ('Qo\'shimcha ma\'lumotlar', {
            'fields': ('notes',),
            'classes': ('collapse',),
        }),
        ('Vaqt ma\'lumotlari', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        })
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_client_name', 'get_client_phone', 'status', 'baklashka_soni', 'kuler_soni', 'created_by', 'assigned_to', 'created_at')
    list_filter = ('status', 'created_at', 'updated_at', 'created_by', 'assigned_to')
    search_fields = ('id', 'client__full_name', 'client__phone_number', 'notes')
    readonly_fields = ('id', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    
    def get_client_name(self, obj):
        return obj.client.full_name if obj.client else '-'  
    get_client_name.short_description = 'Mijoz ismi'
    
    def get_client_phone(self, obj):
        return obj.client.phone_number if obj.client else '-'
    get_client_phone.short_description = 'Telefon raqami'
    
    fieldsets = (
        ('Buyurtma ma\'lumotlari', {
            'fields': ('id', 'client', 'baklashka_soni', 'kuler_soni', 'notes')
        }),
        ('Holat va foydalanuvchilar', {
            'fields': ('status', 'created_by', 'assigned_to')
        }),
        ('Vaqt ma\'lumotlari', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        })
    )
