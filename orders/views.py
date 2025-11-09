from rest_framework import generics, status, permissions, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiExample, OpenApiResponse
from .models import Order, Client
from .serializers import (
    OrderSerializer, 
    OrderCreateSerializer, 
    OrderUpdateSerializer,
    OrderListSerializer,
    ClientSerializer
)


@extend_schema_view(
    list=extend_schema(
        summary="Barcha buyurtmalarni ko'rish",
        description="Tizimda mavjud barcha buyurtmalarni ko'rish. Filter, search va pagination qo'llab-quvvatlanadi.",
        tags=["Orders"]
    ),
    create=extend_schema(
        summary="Yangi buyurtma yaratish",
        description="Yangi buyurtma yaratish. 5-xonali unique ID avtomatik generatsiya qilinadi.",
        request=OrderCreateSerializer,
        responses={
            201: OrderSerializer,
            400: OpenApiResponse(description="Noto'g'ri ma'lumotlar")
        },
        examples=[
            OpenApiExample(
                'Yangi buyurtma',
                value={
                    "client_full_name": "Anvar Karimov",
                    "client_phone_number": "+998901234567",
                    "client_location_name": "Toshkent mall",
                    "client_address": "Toshkent sh., Chilonzor t., 1-kv, 10-uy",
                    "client_longitude": "69.2401",
                    "client_latitude": "41.2995",
                    "client_notes": "Doimiy mijoz",
                    "kiruvchi_soni": 5,
                    "chiquvchi_soni": 3,
                    "notes": "2-qavat, qo'ng'iroq qiling"
                }
            )
        ],
        tags=["Orders"]
    )
)
class OrderListCreateView(generics.ListCreateAPIView):
    """
    Buyurtmalar ro'yxati va yangi buyurtma yaratish
    """
    queryset = Order.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'assigned_to', 'created_by']
    search_fields = ['client__full_name', 'client__phone_number', 'client__location_name', 'notes']
    ordering_fields = ['created_at', 'updated_at', 'status']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrderCreateSerializer
        return OrderListSerializer
    
    def create(self, request, *args, **kwargs):
        """Custom create method to return full order data with ID"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        
        # Full order serializer bilan qaytarish
        response_serializer = OrderSerializer(order, context=self.get_serializer_context())
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


@extend_schema_view(
    retrieve=extend_schema(
        summary="Buyurtma ma'lumotlarini ko'rish",
        description="ID bo'yicha bitta buyurtma ma'lumotlarini to'liq ko'rish",
        tags=["Orders"]
    ),
    update=extend_schema(
        summary="Buyurtma ma'lumotlarini yangilash",
        description="Buyurtma ma'lumotlarini to'liq yangilash (PUT)",
        request=OrderUpdateSerializer,
        responses={
            200: OrderSerializer,
            400: OpenApiResponse(description="Noto'g'ri ma'lumotlar"),
            404: OpenApiResponse(description="Buyurtma topilmadi")
        },
        tags=["Orders"]
    ),
    partial_update=extend_schema(
        summary="Buyurtma ma'lumotlarini qisman yangilash",
        description="Buyurtma ma'lumotlarini qisman yangilash (PATCH)",
        request=OrderUpdateSerializer,
        responses={
            200: OrderSerializer,
            400: OpenApiResponse(description="Noto'g'ri ma'lumotlar"),
            404: OpenApiResponse(description="Buyurtma topilmadi")
        },
        tags=["Orders"]
    ),
    destroy=extend_schema(
        summary="Buyurtmani o'chirish",
        description="Buyurtmani tizimdan butunlay o'chirish",
        responses={
            204: OpenApiResponse(description="Muvaffaqiyatli o'chirildi"),
            404: OpenApiResponse(description="Buyurtma topilmadi")
        },
        tags=["Orders"]
    )
)
class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Bitta buyurtma bilan bog'liq CRUD operatsiyalar
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return OrderUpdateSerializer
        return OrderSerializer


@extend_schema(
    summary="Buyurtma statusini yangilash",
    description="Buyurtma statusini tez yangilash uchun endpoint",
    request={
        'type': 'object',
        'properties': {
            'status': {
                'type': 'string',
                'enum': ['kutilmoqda', 'bajarildi', 'bekor_qilindi'],
                'description': 'Yangi status'
            }
        },
        'required': ['status']
    },
    responses={
        200: OpenApiResponse(
            description="Status muvaffaqiyatli yangilandi",
            examples=[
                OpenApiExample(
                    'Status yangilandi',
                    value={
                        "message": "Buyurtma statusi muvaffaqiyatli yangilandi!",
                        "order_id": 12345,
                        "new_status": "bajarildi"
                    }
                )
            ]
        ),
        400: OpenApiResponse(description="Noto'g'ri status"),
        404: OpenApiResponse(description="Buyurtma topilmadi")
    },
    tags=["Orders"]
)
@api_view(['PATCH'])
@permission_classes([permissions.IsAuthenticated])
def update_order_status(request, pk):
    """
    Buyurtma statusini yangilash
    """
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response(
            {"error": "Buyurtma topilmadi!"}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    new_status = request.data.get('status')
    if not new_status:
        return Response(
            {"error": "Status kiritish majburiy!"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    valid_statuses = ['kutilmoqda', 'bajarildi', 'bekor_qilindi']
    if new_status not in valid_statuses:
        return Response(
            {"error": f"Status {valid_statuses} ichidan birini tanlang!"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    order.status = new_status
    order.save()
    
    return Response({
        "message": "Buyurtma statusi muvaffaqiyatli yangilandi!",
        "order_id": order.id,
        "new_status": order.status
    }, status=status.HTTP_200_OK)


@extend_schema(
    summary="Kuryerga buyurtma tayinlash",
    description="Buyurtmani kuryerga tayinlash yoki tayinlashni bekor qilish",
    request={
        'type': 'object',
        'properties': {
            'courier_id': {
                'type': 'integer',
                'description': 'Kuryer ID si (null bo\'lsa tayinlash bekor qilinadi)',
                'nullable': True
            }
        }
    },
    responses={
        200: OpenApiResponse(
            description="Kuryer muvaffaqiyatli tayinlandi",
            examples=[
                OpenApiExample(
                    'Kuryer tayinlandi',
                    value={
                        "message": "Buyurtma kuryerga muvaffaqiyatli tayinlandi!",
                        "order_id": 12345,
                        "courier_name": "Kuryer Ismi"
                    }
                )
            ]
        ),
        400: OpenApiResponse(description="Noto'g'ri kuryer ID yoki rol"),
        404: OpenApiResponse(description="Buyurtma yoki kuryer topilmadi")
    },
    tags=["Orders"]
)
@api_view(['PATCH'])
@permission_classes([permissions.IsAuthenticated])
def assign_courier(request, pk):
    """
    Buyurtmani kuryerga tayinlash
    """
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response(
            {"error": "Buyurtma topilmadi!"}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    courier_id = request.data.get('courier_id')
    
    if courier_id is None:
        # Tayinlashni bekor qilish
        order.assigned_to = None
        order.save()
        return Response({
            "message": "Kuryer tayinlash bekor qilindi!",
            "order_id": order.id
        }, status=status.HTTP_200_OK)
    
    try:
        from users.models import User
        courier = User.objects.get(pk=courier_id)
        if courier.role != 'kuryer':
            return Response(
                {"error": "Faqat kuryer rolindagi foydalanuvchini tayinlash mumkin!"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    except User.DoesNotExist:
        return Response(
            {"error": "Kuryer topilmadi!"}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    order.assigned_to = courier
    order.save()
    
    return Response({
        "message": "Buyurtma kuryerga muvaffaqiyatli tayinlandi!",
        "order_id": order.id,
        "courier_name": courier.full_name
    }, status=status.HTTP_200_OK)


@extend_schema(
    summary="Mening buyurtmalarim",
    description="Joriy foydalanuvchi yaratgan yoki tayinlangan buyurtmalar",
    responses={200: OrderListSerializer(many=True)},
    tags=["Orders"]
)
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def my_orders(request):
    """
    Joriy foydalanuvchining buyurtmalari
    """
    user = request.user
    
    if user.role == 'kuryer':
        # Kuryer uchun - tayinlangan buyurtmalar
        orders = Order.objects.filter(assigned_to=user)
    else:
        # Admin yoki boshqa rollar uchun - yaratgan buyurtmalar
        orders = Order.objects.filter(created_by=user)
    
    serializer = OrderListSerializer(orders, many=True, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)
