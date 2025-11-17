from rest_framework import serializers
from .models import Order, Client
from users.models import User


class ClientSerializer(serializers.ModelSerializer):
    is_danger = serializers.SerializerMethodField(help_text="1 oydan beri zakaz bermagan mijozlar uchun True, aks holda False")

    def get_is_danger(self, obj):
        from datetime import timedelta
        from django.utils import timezone
        # Oxirgi buyurtmasini topamiz
        last_order = Order.objects.filter(client=obj).order_by('-created_at').first()
        if not last_order or not last_order.created_at:
            return True  # Hech qachon zakaz bermaganlar yoki created_at null bo'lganlar ham xavfli
        # Hozirgi sana
        now = timezone.now().date()
        # created_at endi DateField
        if (now - last_order.created_at).days >= 30:
            return True
        return False
    """
    Client modelini serialize qilish uchun serializer
    """
    class Meta:
        model = Client
        fields = [
            'id', 'full_name', 'phone_number', 'address', 
            'longitude', 'latitude', 'notes', 'created_at', 'updated_at', 'is_danger'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'is_danger']
        extra_kwargs = {
            'full_name': {'help_text': 'Mijozning to\'liq ism-familyasi'},
            'phone_number': {'help_text': 'Mijozning telefon raqami'},
            'address': {'help_text': 'To\'liq manzil'},
            'longitude': {'help_text': 'GPS uzunlik kordinatasi (ixtiyoriy)'},
            'latitude': {'help_text': 'GPS kenglik kordinatasi (ixtiyoriy)'},
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
            'id', 'client', 'client_id', 'baklashka_soni', 'kuler_soni', 'pompa_soni',
            'price', 'notes', 'status', 'created_at', 'updated_at', 'created_by', 
            'assigned_to', 'created_by_username', 'assigned_to_username'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by_username', 'assigned_to_username']
        extra_kwargs = {
            'baklashka_soni': {'help_text': 'Baklashkalar soni'},
            'kuler_soni': {'help_text': 'Kulerlar soni'},
            'pompa_soni': {'help_text': 'Pompa soni'},
            'price': {'help_text': 'Buyurtma narxi (so\'mda)'},
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
    Faqat mavjud mijoz ID si bilan buyurtma yaratish.
    """
    # Mavjud client ID si (majburiy)
    client_id = serializers.IntegerField(
        required=True, 
        help_text="Mavjud mijozning ID raqami"
    )
    
    class Meta:
        model = Order
        fields = [
            'client_id', 'baklashka_soni', 'kuler_soni', 'pompa_soni', 'price', 'notes', 'assigned_to'
        ]
        extra_kwargs = {
            'baklashka_soni': {'help_text': 'Baklashkalar soni (default: 0)'},
            'kuler_soni': {'help_text': 'Kulerlar soni (default: 0)'},
            'pompa_soni': {'help_text': 'Pompa soni (default: 0)'},
            'price': {'help_text': 'Buyurtma narxi (so\'mda)'},
            'notes': {'help_text': 'Buyurtma haqida qo\'shimcha izohlar (ixtiyoriy)'},
            'assigned_to': {'help_text': 'Tayinlangan kuryer (ixtiyoriy)'},
        }
    
    def validate_client_id(self, value):
        """
        Client ID validatsiyasi
        """
        try:
            Client.objects.get(id=value)
        except Client.DoesNotExist:
            raise serializers.ValidationError(f"ID={value} bo'lgan mijoz topilmadi!")
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
        Yangi buyurtma yaratish (faqat mavjud mijoz bilan)
        """
        client_id = validated_data.pop('client_id')
        client = Client.objects.get(id=client_id)
        
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
            'client_id', 'baklashka_soni', 'kuler_soni', 'pompa_soni', 'price',
            'notes', 'status', 'assigned_to'
        ]
        extra_kwargs = {
            'baklashka_soni': {'help_text': 'Baklashkalar soni'},
            'kuler_soni': {'help_text': 'Kulerlar soni'},
            'pompa_soni': {'help_text': 'Pompa soni'},
            'price': {'help_text': 'Buyurtma narxi (so\'mda)'},
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
    client_id = serializers.IntegerField(source='client.id', read_only=True)
    assigned_id = serializers.IntegerField(source='assigned_to.id', read_only=True)
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
    client_address = serializers.CharField(
        source='client.address', 
        read_only=True
    )
    client_longitude = serializers.DecimalField(
        source='client.longitude',
        max_digits=10,
        decimal_places=7,
        read_only=True
    )
    client_latitude = serializers.DecimalField(
        source='client.latitude',
        max_digits=10,
        decimal_places=7,
        read_only=True
    )

    class Meta:
        model = Order
        fields = [
            'id', 'client_id', 'assigned_id',
            'client_full_name', 'client_phone_number', 'client_address',
            'client_longitude', 'client_latitude', 'status', 'baklashka_soni', 'kuler_soni', 'pompa_soni', 'price',
            'created_at', 'updated_at', 'created_by_username', 'assigned_to_username'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']