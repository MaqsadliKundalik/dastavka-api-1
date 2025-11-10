from rest_framework import serializers
from .models import Order, Client
from users.models import User


class ClientSerializer(serializers.ModelSerializer):
    """
    Client modelini serialize qilish uchun serializer
    """
    class Meta:
        model = Client
        fields = [
            'id', 'full_name', 'phone_number', 'location_name', 'address', 
            'longitude', 'latitude', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {
            'full_name': {'help_text': 'Mijozning to\'liq ism-familyasi'},
            'phone_number': {'help_text': 'Mijozning telefon raqami'},
            'location_name': {'help_text': 'Joylashuv nomi (masalan: "Toshkent mall")'},
            'address': {'help_text': 'To\'liq manzil'},
            'longitude': {'help_text': 'Geografik uzunlik (ixtiyoriy)'},
            'latitude': {'help_text': 'Geografik kenglik (ixtiyoriy)'},
            'notes': {'help_text': 'Mijoz haqida qo\'shimcha ma\'lumotlar (ixtiyoriy)'},
        }
    
    def validate_phone_number(self, value):
        """
        Telefon raqam validatsiyasi
        """
        if not value.replace('+', '').replace('-', '').replace(' ', '').replace('(', '').replace(')', '').isdigit():
            raise serializers.ValidationError("Telefon raqam faqat raqamlardan iborat bo'lishi kerak!")
        return value


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
    client = ClientSerializer(read_only=True)
    client_id = serializers.IntegerField(write_only=True, help_text="Mijoz ID raqami")
    
    class Meta:
        model = Order
        fields = [
            'id', 'client', 'client_id', 'kiruvchi_soni', 'chiquvchi_soni',
            'notes', 'status', 'created_at', 'updated_at', 'created_by', 
            'assigned_to', 'created_by_username', 'assigned_to_username'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by_username', 'assigned_to_username']
        extra_kwargs = {
            'kiruvchi_soni': {'help_text': 'Kiruvchi buyumlar soni'},
            'chiquvchi_soni': {'help_text': 'Chiquvchi buyumlar soni'},
            'notes': {'help_text': 'Buyurtma haqida qo\'shimcha izohlar (ixtiyoriy)'},
            'status': {'help_text': 'Buyurtma holati'},
            'assigned_to': {'help_text': 'Tayinlangan kuryer (ixtiyoriy)'},
        }
    
    def validate_client_id(self, value):
        """
        Client ID validatsiyasi
        """
        try:
            Client.objects.get(id=value)
        except Client.DoesNotExist:
            raise serializers.ValidationError("Bunday ID raqamli mijoz topilmadi!")
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
    Yangi buyurtma yaratish uchun serializer.
    Ikki xil usul bilan buyurtma yaratish mumkin:
    1. client_id kiritish (mavjud mijoz uchun)
    2. client ma'lumotlarini kiritish (yangi mijoz yaratish uchun)
    """
    # Mavjud client ID si (ixtiyoriy)
    client_id = serializers.IntegerField(
        required=False, 
        help_text="Mavjud mijozning ID raqami (agar mavjud mijoz uchun buyurtma bersa)"
    )
    
    # Yangi client ma'lumotlari (ixtiyoriy)
    client_full_name = serializers.CharField(
        required=False, 
        help_text="Yangi mijozning to'liq ism-familyasi"
    )
    client_phone_number = serializers.CharField(
        required=False, 
        help_text="Yangi mijozning telefon raqami"
    )
    client_location_name = serializers.CharField(
        required=False, 
        help_text="Yangi mijozning joylashuv nomi"
    )
    client_address = serializers.CharField(
        required=False, 
        help_text="Yangi mijozning to'liq manzili"
    )
    client_longitude = serializers.DecimalField(
        max_digits=10, 
        decimal_places=7, 
        required=False, 
        help_text="Yangi mijozning geografik uzunligi (ixtiyoriy)"
    )
    client_latitude = serializers.DecimalField(
        max_digits=10, 
        decimal_places=7, 
        required=False, 
        help_text="Yangi mijozning geografik kengligi (ixtiyoriy)"
    )
    client_notes = serializers.CharField(
        required=False, 
        allow_blank=True, 
        help_text="Yangi mijoz haqida qo'shimcha ma'lumotlar (ixtiyoriy)"
    )
    
    class Meta:
        model = Order
        fields = [
            'client_id',
            'client_full_name', 'client_phone_number', 'client_location_name', 
            'client_address', 'client_longitude', 'client_latitude', 'client_notes',
            'kiruvchi_soni', 'chiquvchi_soni', 'notes', 'assigned_to'
        ]
        extra_kwargs = {
            'kiruvchi_soni': {'help_text': 'Kiruvchi buyumlar soni (default: 0)'},
            'chiquvchi_soni': {'help_text': 'Chiquvchi buyumlar soni (default: 0)'},
            'notes': {'help_text': 'Buyurtma haqida qo\'shimcha izohlar (ixtiyoriy)'},
            'assigned_to': {'help_text': 'Tayinlangan kuryer (ixtiyoriy)'},
        }
    
    def validate(self, data):
        """
        Ma'lumotlarni to'liq validatsiya qilish
        """
        client_id = data.get('client_id')
        client_full_name = data.get('client_full_name')
        
        # Client ID yoki yangi client ma'lumotlari majburiy
        if not client_id and not client_full_name:
            raise serializers.ValidationError(
                "client_id (mavjud mijoz uchun) yoki client_full_name (yangi mijoz uchun) kiritish majburiy!"
            )
        
        # Agar client_id berilgan bo'lsa, boshqa client fieldlari kerak emas
        if client_id:
            try:
                Client.objects.get(id=client_id)
            except Client.DoesNotExist:
                raise serializers.ValidationError(f"ID={client_id} bo'lgan mijoz topilmadi!")
        
        # Agar yangi client yaratish kerak bo'lsa, majburiy fieldlarni tekshirish
        if not client_id and client_full_name:
            required_fields = ['client_phone_number', 'client_location_name', 'client_address']
            for field in required_fields:
                if not data.get(field):
                    raise serializers.ValidationError(f"Yangi mijoz uchun {field} majburiy!")
        
        return data
    
    def validate_client_phone_number(self, value):
        """
        Telefon raqam validatsiyasi
        """
        if value and not value.replace('+', '').replace('-', '').replace(' ', '').replace('(', '').replace(')', '').isdigit():
            raise serializers.ValidationError("Telefon raqam faqat raqamlardan iborat bo'lishi kerak!")
        return value
    
    def validate_assigned_to(self, value):
        """
        Faqat kuryer rolida bo'lgan userlarni tayinlash mumkin
        """
        if value and value.role != 'kuryer':
            raise serializers.ValidationError("Faqat kuryer rolindagilarni tayinlash mumkin!")
        return value
    
    def create(self, validated_data):
        """
        Yangi buyurtma yaratish (mavjud yoki yangi mijoz bilan)
        """
        client_id = validated_data.pop('client_id', None)
        client = None
        
        if client_id:
            # Mavjud mijozni olish
            client = Client.objects.get(id=client_id)
            
            # Client ma'lumotlarini o'chirish (ular kerak emas)
            validated_data.pop('client_full_name', None)
            validated_data.pop('client_phone_number', None)
            validated_data.pop('client_location_name', None)
            validated_data.pop('client_address', None)
            validated_data.pop('client_longitude', None)
            validated_data.pop('client_latitude', None)
            validated_data.pop('client_notes', None)
        else:
            # Yangi mijoz yaratish
            client_data = {
                'full_name': validated_data.pop('client_full_name'),
                'phone_number': validated_data.pop('client_phone_number'),
                'location_name': validated_data.pop('client_location_name'),
                'address': validated_data.pop('client_address'),
                'longitude': validated_data.pop('client_longitude', None),
                'latitude': validated_data.pop('client_latitude', None),
                'notes': validated_data.pop('client_notes', ''),
            }
            client = Client.objects.create(**client_data)
        
        # Buyurtma ma'lumotlarini tayyorlash
        validated_data['client'] = client
        
        # Yaratuvchini request.user dan olish
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            validated_data['created_by'] = request.user
        
        return super().create(validated_data)


class OrderUpdateSerializer(serializers.ModelSerializer):
    """
    Buyurtmani yangilash uchun serializer
    """
    client_id = serializers.IntegerField(
        required=False, 
        help_text="Mijozni o'zgartirish uchun mijoz ID raqami (ixtiyoriy)"
    )
    
    class Meta:
        model = Order
        fields = [
            'client_id', 'kiruvchi_soni', 'chiquvchi_soni',
            'notes', 'status', 'assigned_to'
        ]
        extra_kwargs = {
            'kiruvchi_soni': {'help_text': 'Kiruvchi buyumlar soni'},
            'chiquvchi_soni': {'help_text': 'Chiquvchi buyumlar soni'},
            'notes': {'help_text': 'Buyurtma haqida qo\'shimcha izohlar'},
            'status': {'help_text': 'Buyurtma holati'},
            'assigned_to': {'help_text': 'Tayinlangan kuryer'},
        }
    
    def validate_client_id(self, value):
        """
        Client ID validatsiyasi
        """
        if value:
            try:
                Client.objects.get(id=value)
            except Client.DoesNotExist:
                raise serializers.ValidationError("Bunday ID raqamli mijoz topilmadi!")
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
    client_full_name = serializers.CharField(
        source='client.full_name', 
        read_only=True
    )
    client_phone_number = serializers.CharField(
        source='client.phone_number', 
        read_only=True
    )
    client_location_name = serializers.CharField(
        source='client.location_name', 
        read_only=True
    )
    
    class Meta:
        model = Order
        fields = [
            'id', 'client_full_name', 'client_phone_number', 'client_location_name',
            'status', 'kiruvchi_soni', 'chiquvchi_soni', 
            'created_at', 'updated_at', 'created_by_username', 'assigned_to_username'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']