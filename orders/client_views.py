from rest_framework import generics, status, permissions, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiExample, OpenApiResponse
from .models import Client
from .serializers import ClientSerializer


@extend_schema_view(
    list=extend_schema(
        summary="Barcha mijozlarni ko'rish",
        description="Tizimda ro'yxatdan o'tgan barcha mijozlarni ko'rish. Filter, search va pagination qo'llab-quvvatlanadi.",
        tags=["Clients"]
    ),
    create=extend_schema(
        summary="Yangi mijoz yaratish",
        description="Yangi mijoz ro'yxatdan o'tkazish",
        request=ClientSerializer,
        responses={
            201: ClientSerializer,
            400: OpenApiResponse(description="Noto'g'ri ma'lumotlar")
        },
        examples=[
            OpenApiExample(
                'Yangi mijoz',
                value={
                    "full_name": "Anvar Karimov",
                    "phone_number": "+998901234567",
                    "location_name": "Toshkent Mall",
                    "address": "Toshkent sh., Chilonzor t., 1-kv, 10-uy",
                    "longitude": "69.2401",
                    "latitude": "41.2995",
                    "notes": "Doimiy mijoz"
                }
            )
        ],
        tags=["Clients"]
    )
)
class ClientListCreateView(generics.ListCreateAPIView):
    """
    Mijozlar ro'yxati va yangi mijoz yaratish
    """
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['full_name', 'phone_number', 'location_name', 'address']
    ordering_fields = ['created_at', 'updated_at', 'full_name']
    ordering = ['-created_at']


@extend_schema_view(
    retrieve=extend_schema(
        summary="Mijoz ma'lumotlarini ko'rish",
        description="ID bo'yicha bitta mijoz ma'lumotlarini to'liq ko'rish",
        tags=["Clients"]
    ),
    update=extend_schema(
        summary="Mijoz ma'lumotlarini yangilash",
        description="Mijoz ma'lumotlarini to'liq yangilash (PUT)",
        request=ClientSerializer,
        responses={
            200: ClientSerializer,
            400: OpenApiResponse(description="Noto'g'ri ma'lumotlar"),
            404: OpenApiResponse(description="Mijoz topilmadi")
        },
        tags=["Clients"]
    ),
    partial_update=extend_schema(
        summary="Mijoz ma'lumotlarini qisman yangilash",
        description="Mijoz ma'lumotlarini qisman yangilash (PATCH)",
        request=ClientSerializer,
        responses={
            200: ClientSerializer,
            400: OpenApiResponse(description="Noto'g'ri ma'lumotlar"),
            404: OpenApiResponse(description="Mijoz topilmadi")
        },
        tags=["Clients"]
    ),
    destroy=extend_schema(
        summary="Mijozni o'chirish",
        description="Mijozni tizimdan butunlay o'chirish (barcha buyurtmalari bilan birga)",
        responses={
            204: OpenApiResponse(description="Muvaffaqiyatli o'chirildi"),
            404: OpenApiResponse(description="Mijoz topilmadi")
        },
        tags=["Clients"]
    )
)
class ClientDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Bitta mijoz bilan bog'liq CRUD operatsiyalar
    """
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.AllowAny]


@extend_schema(
    summary="Mijozning buyurtmalari",
    description="Bitta mijozning barcha buyurtmalarini ko'rish",
    responses={200: 'OrderListSerializer(many=True)'},
    tags=["Clients"]
)
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def client_orders(request, pk):
    """
    Mijozning barcha buyurtmalari
    """
    try:
        client = Client.objects.get(pk=pk)
    except Client.DoesNotExist:
        return Response(
            {"error": "Mijoz topilmadi!"}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    orders = client.orders.all().order_by('-created_at')
    
    # OrderListSerializer import qilish
    from .serializers import OrderListSerializer
    serializer = OrderListSerializer(orders, many=True, context={'request': request})
    
    return Response({
        "client": ClientSerializer(client, context={'request': request}).data,
        "orders_count": orders.count(),
        "orders": serializer.data
    }, status=status.HTTP_200_OK)


@extend_schema(
    summary="Mijozlar statistikasi",
    description="Mijozlar haqida umumiy statistika",
    responses={
        200: OpenApiResponse(
            description="Statistika ma'lumotlari",
            examples=[
                OpenApiExample(
                    'Statistika',
                    value={
                        "total_clients": 150,
                        "active_clients": 120,
                        "clients_with_orders": 100,
                        "top_clients": [
                            {
                                "id": 1,
                                "full_name": "Anvar Karimov",
                                "orders_count": 25
                            }
                        ]
                    }
                )
            ]
        )
    },
    tags=["Clients"]
)
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def clients_stats(request):
    """
    Mijozlar statistikasi
    """
    from django.db.models import Count
    
    total_clients = Client.objects.count()
    clients_with_orders = Client.objects.filter(orders__isnull=False).distinct().count()
    
    # Eng ko'p buyurtma bergan mijozlar (top 10)
    top_clients = Client.objects.annotate(
        orders_count=Count('orders')
    ).filter(orders_count__gt=0).order_by('-orders_count')[:10]
    
    top_clients_data = []
    for client in top_clients:
        top_clients_data.append({
            "id": client.id,
            "full_name": client.full_name,
            "phone_number": client.phone_number,
            "orders_count": client.orders_count
        })
    
    return Response({
        "total_clients": total_clients,
        "clients_with_orders": clients_with_orders,
        "clients_without_orders": total_clients - clients_with_orders,
        "top_clients": top_clients_data
    }, status=status.HTTP_200_OK)