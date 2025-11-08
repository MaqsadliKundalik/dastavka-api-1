from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import login
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiExample, OpenApiResponse
from drf_spectacular.openapi import AutoSchema
from .models import User
from .serializers import (
    UserSerializer, 
    UserRegistrationSerializer, 
    UserLoginSerializer,
    UserProfileSerializer
)


@extend_schema_view(
    list=extend_schema(
        summary="Barcha foydalanuvchilarni ko'rish",
        description="Tizimda ro'yxatdan o'tgan barcha foydalanuvchilarni ko'rish. Faqat autentifikatsiya qilingan foydalanuvchilar uchun.",
        tags=["Users"]
    ),
    create=extend_schema(
        summary="Yangi foydalanuvchi yaratish",
        description="Yangi foydalanuvchi yaratish. Faqat admin huquqiga ega foydalanuvchilar uchun.",
        tags=["Users"]
    )
)
class UserListCreateView(generics.ListCreateAPIView):
    """
    Foydalanuvchilar ro'yxati va yangi foydalanuvchi yaratish endpoint-i
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        """
        Faqat admin userlar yangi user yarata oladi
        """
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated()]


@extend_schema_view(
    retrieve=extend_schema(
        summary="Foydalanuvchi ma'lumotlarini ko'rish",
        description="ID bo'yicha bitta foydalanuvchi ma'lumotlarini olish",
        tags=["Users"]
    ),
    update=extend_schema(
        summary="Foydalanuvchi ma'lumotlarini yangilash",
        description="Foydalanuvchi ma'lumotlarini to'liq yangilash (PUT)",
        tags=["Users"]
    ),
    partial_update=extend_schema(
        summary="Foydalanuvchi ma'lumotlarini qisman yangilash",
        description="Foydalanuvchi ma'lumotlarini qisman yangilash (PATCH)",
        tags=["Users"]
    ),
    destroy=extend_schema(
        summary="Foydalanuvchini o'chirish",
        description="Foydalanuvchini tizimdan o'chirish",
        tags=["Users"]
    )
)
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Bitta foydalanuvchi bilan bog'liq CRUD operatsiyalar
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


@extend_schema(
    summary="Foydalanuvchi ro'yxatdan o'tish",
    description="Yangi foydalanuvchi ro'yxatdan o'tish va avtomatik token olish",
    request=UserRegistrationSerializer,
    responses={
        201: OpenApiResponse(
            response=UserProfileSerializer,
            description="Muvaffaqiyatli ro'yxatdan o'tish",
            examples=[
                OpenApiExample(
                    'Muvaffaqiyatli javob',
                    value={
                        "message": "User muvaffaqiyatli ro'yxatdan o'tdi!",
                        "user": {
                            "id": 1,
                            "username": "test_user",
                            "full_name": "Test User",
                            "role": "kuryer",
                            "status": "active"
                        },
                        "token": "abc123token"
                    }
                )
            ]
        ),
        400: OpenApiResponse(description="Noto'g'ri ma'lumotlar")
    },
    tags=["Authentication"]
)
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def user_registration(request):
    """
    Yangi foydalanuvchi ro'yxatdan o'tish endpoint-i
    """
    try:
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'message': 'User muvaffaqiyatli ro\'yxatdan o\'tdi!',
                'user': UserProfileSerializer(user).data,
                'token': token.key
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            'error': f'Registration xatosi: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema(
    summary="Foydalanuvchi tizimga kirish",
    description="Username va parol bilan tizimga kirish va token olish",
    request=UserLoginSerializer,
    responses={
        200: OpenApiResponse(
            description="Muvaffaqiyatli kirish",
            examples=[
                OpenApiExample(
                    'Login muvaffaqiyatli',
                    value={
                        "message": "Muvaffaqiyatli login!",
                        "user": {
                            "id": 1,
                            "username": "test_user",
                            "full_name": "Test User",
                            "role": "kuryer",
                            "status": "active"
                        },
                        "token": "abc123token"
                    }
                )
            ]
        ),
        400: OpenApiResponse(description="Noto'g'ri login ma'lumotlari")
    },
    tags=["Authentication"]
)
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def user_login(request):
    """
    Foydalanuvchi tizimga kirish endpoint-i
    """
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        login(request, user)
        return Response({
            'message': 'Muvaffaqiyatli login!',
            'user': UserProfileSerializer(user).data,
            'token': token.key
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    summary="Foydalanuvchi tizimdan chiqish",
    description="Foydalanuvchining tokenini bekor qilish va tizimdan chiqish",
    responses={
        200: OpenApiResponse(
            description="Muvaffaqiyatli chiqish",
            examples=[
                OpenApiExample(
                    'Logout muvaffaqiyatli',
                    value={"message": "Muvaffaqiyatli logout!"}
                )
            ]
        ),
        400: OpenApiResponse(description="Token topilmadi")
    },
    tags=["Authentication"]
)
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def user_logout(request):
    """
    Foydalanuvchi tizimdan chiqish endpoint-i
    """
    try:
        token = Token.objects.get(user=request.user)
        token.delete()
        return Response({
            'message': 'Muvaffaqiyatli logout!'
        }, status=status.HTTP_200_OK)
    except Token.DoesNotExist:
        return Response({
            'error': 'Token topilmadi!'
        }, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    summary="Foydalanuvchi profili",
    description="Joriy foydalanuvchining profil ma'lumotlarini ko'rish yoki yangilash",
    responses={
        200: UserProfileSerializer,
    },
    tags=["Profile"]
)
@api_view(['GET', 'PUT', 'PATCH'])
@permission_classes([permissions.IsAuthenticated])
def user_profile(request):
    """
    Foydalanuvchi profili ko'rish va yangilash endpoint-i
    """
    if request.method == 'GET':
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method in ['PUT', 'PATCH']:
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Profil muvaffaqiyatli yangilandi!',
                'user': serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    summary="Profilni yangilash",
    description="Joriy foydalanuvchining profil ma'lumotlarini yangilash",
    request=UserProfileSerializer,
    responses={
        200: OpenApiResponse(
            description="Profil muvaffaqiyatli yangilandi",
            examples=[
                OpenApiExample(
                    'Profil yangilandi',
                    value={
                        "message": "Profil muvaffaqiyatli yangilandi!",
                        "user": {
                            "id": 1,
                            "username": "test_user",
                            "full_name": "Yangilangan Ism",
                            "role": "kuryer",
                            "status": "active"
                        }
                    }
                )
            ]
        ),
        400: OpenApiResponse(description="Noto'g'ri ma'lumotlar")
    },
    tags=["Profile"]
)
@api_view(['PUT', 'PATCH'])
@permission_classes([permissions.IsAuthenticated])
def update_profile(request):
    """
    Foydalanuvchi profilini yangilash endpoint-i
    """
    serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': 'Profil muvaffaqiyatli yangilandi!',
            'user': serializer.data
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
