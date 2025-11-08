from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Foydalanuvchi ma'lumotlarini serialize qilish uchun serializer.
    Barcha CRUD operatsiyalar uchun ishlatiladi.
    """
    password = serializers.CharField(
        write_only=True, 
        min_length=8,
        help_text="Kamida 8 ta belgi bo'lishi kerak",
        style={'input_type': 'password'}
    )
    
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'full_name', 'role', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {
            'password': {'write_only': True},
        }
    
    def create(self, validated_data):
        """
        Yangi user yaratish
        """
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        return user
    
    def update(self, instance, validated_data):
        """
        User ma'lumotlarini yangilash
        """
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if password:
            instance.set_password(password)
        
        instance.save()
        return instance


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Yangi foydalanuvchi ro'yxatdan o'tish uchun serializer.
    Parol tasdiqlash va validatsiya mavjud.
    """
    password = serializers.CharField(
        write_only=True, 
        min_length=8,
        help_text="Kamida 8 ta belgi bo'lishi kerak",
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True,
        help_text="Parolni tasdiqlash uchun",
        style={'input_type': 'password'}
    )
    
    class Meta:
        model = User
        fields = ['username', 'password', 'password_confirm', 'full_name', 'role']
    
    def validate(self, data):
        """
        Parollarni tekshirish
        """
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Parollar mos kelmaydi!")
        
        # Username unique ekanligini tekshirish
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError("Bu username allaqachon mavjud!")
        
        return data
    
    def create(self, validated_data):
        """
        Yangi user yaratish
        """
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        
        # Email field ni olib tashlash (agar mavjud bo'lsa)
        validated_data.pop('email', None)
        
        # User yaratish va parolni hash qilish
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    Foydalanuvchi tizimga kirish uchun serializer.
    Username va parol orqali autentifikatsiya.
    """
    username = serializers.CharField(
        help_text="Foydalanuvchi nomi",
        style={'placeholder': 'Username kiriting'}
    )
    password = serializers.CharField(
        write_only=True,
        help_text="Parol",
        style={'input_type': 'password', 'placeholder': 'Parol kiriting'}
    )
    
    def validate(self, data):
        """
        Login ma'lumotlarini tekshirish
        """
        username = data.get('username')
        password = data.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError("Login yoki parol noto'g'ri!")
            
            if user.status != 'active':
                raise serializers.ValidationError("Sizning hisobingiz faol emas!")
                
            data['user'] = user
            return data
        else:
            raise serializers.ValidationError("Username va parol kiritish majburiy!")


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Foydalanuvchi profili ko'rish va yangilash uchun serializer.
    Parol maydonisiz, xavfsiz profil ma'lumotlari.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'full_name', 'role', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'username', 'created_at', 'updated_at']
        extra_kwargs = {
            'full_name': {'help_text': 'To\'liq ism-familya'},
            'role': {'help_text': 'Foydalanuvchi roli (admin/kuryer)'},
            'status': {'help_text': 'Hisobning holati (active/inactive)'},
        }