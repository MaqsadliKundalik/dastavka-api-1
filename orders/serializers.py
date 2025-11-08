from rest_framework import serializers
from .models import Order
from users.models import User


class OrderSerializer(serializers.ModelSerializer):
    """
    Order modelini serialize qilish uchun asosiy serializer
    """
    created_by_username = serializers.CharField(
        source='created_by.username', 
        read_only=True,
        help_text="Yaratuvchi foydalanuvchi nomi"
    )
    assigned_to_username = serializers.CharField(
        source='assigned_to.username', 
        read_only=True,
        help_text="Tayinlangan kuryer nomi"
    )
    
    class Meta:
        model = Order
        fields = [
            'id', 'full_name', 'phone_number', 'address', 'kiruvchi_soni', 'chiquvchi_soni',
            'notes', 'longitude', 'latitude', 'status', 'created_at', 
            'updated_at', 'created_by', 'assigned_to', 'created_by_username',
            'assigned_to_username'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by_username', 'assigned_to_username']
        extra_kwargs = {
            'full_name': {'help_text': 'Mijozning to\'liq ism-familyasi'},
            'phone_number': {'help_text': 'Mijozning telefon raqami'},
            'address': {'help_text': 'Dastavka manzili'},
            'kiruvchi_soni': {'help_text': 'Kiruvchi buyumlar soni'},
            'chiquvchi_soni': {'help_text': 'Chiquvchi buyumlar soni'},
            'notes': {'help_text': 'Qo\'shimcha izohlar (ixtiyoriy)'},
            'longitude': {'help_text': 'Geografik uzunlik (ixtiyoriy)'},
            'latitude': {'help_text': 'Geografik kenglik (ixtiyoriy)'},
            'status': {'help_text': 'Buyurtma holati'},
            'assigned_to': {'help_text': 'Tayinlangan kuryer (ixtiyoriy)'},
        }
    
    def validate_phone_number(self, value):
        """
        Telefon raqam validatsiyasi
        """
        if not value.replace('+', '').replace('-', '').replace(' ', '').replace('(', '').replace(')', '').isdigit():
            raise serializers.ValidationError("Telefon raqam faqat raqamlardan iborat bo'lishi kerak!")
        return value
    
    def validate_assigned_to(self, value):
        """
        Faqat kuryer rolida bo'lgan userlarni tayinlash mumkin
        """
        if value and value.role != 'kuryer':
            raise serializers.ValidationError("Faqat kuryer rolindagi foydalanuvchilarni tayinlash mumkin!")
        return value


class OrderCreateSerializer(serializers.ModelSerializer):
    """
    Yangi buyurtma yaratish uchun serializer
    """
    class Meta:
        model = Order
        fields = [
            'full_name', 'phone_number', 'address', 'kiruvchi_soni', 'chiquvchi_soni',
            'notes', 'longitude', 'latitude', 'assigned_to'
        ]
        extra_kwargs = {
            'full_name': {'help_text': 'Mijozning to\'liq ism-familyasi (majburiy)'},
            'phone_number': {'help_text': 'Mijozning telefon raqami (majburiy)'},
            'address': {'help_text': 'Dastavka manzili (majburiy)'},
            'kiruvchi_soni': {'help_text': 'Kiruvchi buyumlar soni (default: 0)'},
            'chiquvchi_soni': {'help_text': 'Chiquvchi buyumlar soni (default: 0)'},
            'notes': {'help_text': 'Qo\'shimcha izohlar (ixtiyoriy)'},
            'longitude': {'help_text': 'Geografik uzunlik (ixtiyoriy)'},
            'latitude': {'help_text': 'Geografik kenglik (ixtiyoriy)'},
            'assigned_to': {'help_text': 'Tayinlangan kuryer (ixtiyoriy)'},
        }
    
    def validate_phone_number(self, value):
        """
        Telefon raqam validatsiyasi
        """
        if not value.replace('+', '').replace('-', '').replace(' ', '').replace('(', '').replace(')', '').isdigit():
            raise serializers.ValidationError("Telefon raqam faqat raqamlardan iborat bo'lishi kerak!")
        return value
    
    def validate_assigned_to(self, value):
        """
        Faqat kuryer rolida bo'lgan userlarni tayinlash mumkin
        """
        if value and value.role != 'kuryer':
            raise serializers.ValidationError("Faqat kuryer rolindagi foydalanuvchilarni tayinlash mumkin!")
        return value
    
    def create(self, validated_data):
        """
        Yangi buyurtma yaratish
        """
        # Yaratuvchini request.user dan olish
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['created_by'] = request.user
        
        return super().create(validated_data)


class OrderUpdateSerializer(serializers.ModelSerializer):
    """
    Buyurtmani yangilash uchun serializer
    """
    class Meta:
        model = Order
        fields = [
            'full_name', 'phone_number', 'address', 'kiruvchi_soni', 'chiquvchi_soni',
            'notes', 'longitude', 'latitude', 'status', 'assigned_to'
        ]
        extra_kwargs = {
            'full_name': {'help_text': 'Mijozning to\'liq ism-familyasi'},
            'phone_number': {'help_text': 'Mijozning telefon raqami'},
            'address': {'help_text': 'Dastavka manzili'},
            'kiruvchi_soni': {'help_text': 'Kiruvchi buyumlar soni'},
            'chiquvchi_soni': {'help_text': 'Chiquvchi buyumlar soni'},
            'notes': {'help_text': 'Qo\'shimcha izohlar'},
            'longitude': {'help_text': 'Geografik uzunlik'},
            'latitude': {'help_text': 'Geografik kenglik'},
            'status': {'help_text': 'Buyurtma holati'},
            'assigned_to': {'help_text': 'Tayinlangan kuryer'},
        }
    
    def validate_phone_number(self, value):
        """
        Telefon raqam validatsiyasi
        """
        if not value.replace('+', '').replace('-', '').replace(' ', '').replace('(', '').replace(')', '').isdigit():
            raise serializers.ValidationError("Telefon raqam faqat raqamlardan iborat bo'lishi kerak!")
        return value
    
    def validate_assigned_to(self, value):
        """
        Faqat kuryer rolida bo'lgan userlarni tayinlash mumkin
        """
        if value and value.role != 'kuryer':
            raise serializers.ValidationError("Faqat kuryer rolindagi foydalanuvchilarni tayinlash mumkin!")
        return value


class OrderListSerializer(serializers.ModelSerializer):
    """
    Buyurtmalar ro'yxati uchun qisqartirilgan serializer
    """
    created_by_username = serializers.CharField(
        source='created_by.username', 
        read_only=True
    )
    assigned_to_username = serializers.CharField(
        source='assigned_to.username', 
        read_only=True
    )
    
    class Meta:
        model = Order
        fields = [
            'id', 'full_name', 'phone_number', 'address', 'status',
            'kiruvchi_soni', 'chiquvchi_soni', 'created_at', 'updated_at', 'created_by_username',
            'assigned_to_username'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']