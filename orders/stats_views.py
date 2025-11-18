from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Count, Sum, Q, Max
from django.utils import timezone
from datetime import datetime, timedelta, date
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, OpenApiResponse
from drf_spectacular.openapi import OpenApiTypes
from .models import Order, Client
from users.models import User
from .stats_serializers import OrderStatsSerializer, OrderStatsResponseSerializer, DailyStatsSerializer
from .advanced_stats_serializers import TopClientsResponseSerializer, CouriersStatsResponseSerializer


def get_period_dates(period):
    """
    Davr asosida boshlanish va tugash sanalarini qaytaradi
    """
    now = timezone.now()
    today = now.date()
    
    if period == 'today':
        start_date = datetime.combine(today, datetime.min.time())
        end_date = datetime.combine(today, datetime.max.time())
        period_name = "Bugun"
    elif period == 'week':
        # Haftaning dushanba kunidan boshlaymiz
        days_since_monday = today.weekday()
        monday = today - timedelta(days=days_since_monday)
        start_date = datetime.combine(monday, datetime.min.time())
        end_date = now
        period_name = "Shu hafta"
    elif period == 'month':
        # Oyning birinchi kunidan boshlaymiz  
        first_day = today.replace(day=1)
        start_date = datetime.combine(first_day, datetime.min.time())
        end_date = now
        period_name = "Shu oy"
    else:
        # Default: bugun
        start_date = datetime.combine(today, datetime.min.time())
        end_date = datetime.combine(today, datetime.max.time())
        period_name = "Bugun"
    
    # Timezone-aware qilamiz
    if timezone.is_naive(start_date):
        start_date = timezone.make_aware(start_date)
    if timezone.is_naive(end_date):
        end_date = timezone.make_aware(end_date)
    
    return start_date, end_date, period_name


def calculate_order_stats(queryset, period_name, start_date, end_date):
    """
    Buyurtmalar statistikasini hisoblash
    """
    # Asosiy statistika
    total_orders = queryset.count()
    
    # Status bo'yicha taqsimot
    pending_orders = queryset.filter(status='pending').count()
    in_progress_orders = queryset.filter(status='in_progress').count()
    completed_orders = queryset.filter(status='completed').count()
    cancelled_orders = queryset.filter(status='cancelled').count()
    
    # Baklashka, kuler va narx yig'indilari
    aggregates = queryset.aggregate(
        total_baklashka=Sum('baklashka_soni'),
        total_kuler=Sum('kuler_soni'),
        total_pompa=Sum('pompa_soni'),
        total_price=Sum('price')
    )
    return {
        'period': period_name,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'in_progress_orders': in_progress_orders,
        'completed_orders': completed_orders,
        'cancelled_orders': cancelled_orders,
        'total_baklashka': aggregates['total_baklashka'] or 0,
        'total_kuler': aggregates['total_kuler'] or 0,
        'total_pompa': aggregates['total_pompa'] or 0,
        'total_price': aggregates['total_price'] or 0,
        'start_date': start_date,
        'end_date': end_date
    }


def get_daily_breakdown(start_date, end_date):
    """
    Kunlik taqsimot uchun ma'lumotlar
    """
    daily_stats = []
    current_date = start_date.date()
    end_date_only = end_date.date()
    
    while current_date <= end_date_only:
        # Kun davomidagi buyurtmalar
        day_start = datetime.combine(current_date, datetime.min.time())
        day_end = datetime.combine(current_date, datetime.max.time())
        
        if timezone.is_naive(day_start):
            day_start = timezone.make_aware(day_start)
        if timezone.is_naive(day_end):
            day_end = timezone.make_aware(day_end)
        
        day_orders = Order.objects.filter(
            created_at__range=[day_start, day_end]
        )
        
        day_completed = Order.objects.filter(
            updated_at__range=[day_start, day_end],
            status='completed'
        )
        
        aggregates = day_orders.aggregate(
            total_baklashka=Sum('baklashka_soni'),
            total_kuler=Sum('kuler_soni'),
            total_pompa=Sum('pompa_soni'),
            total_price=Sum('price')
        )
        daily_stats.append({
            'date': current_date,
            'total_orders': day_orders.count(),
            'completed_orders': day_completed.count(),
            'total_baklashka': aggregates['total_baklashka'] or 0,
            'total_kuler': aggregates['total_kuler'] or 0,
            'total_pompa': aggregates['total_pompa'] or 0,
            'total_price': aggregates['total_price'] or 0,
        })
        
        current_date += timedelta(days=1)
    
    return daily_stats


@extend_schema(
    summary="Buyurtmalar statistikasi",
    description="Belgilangan davr uchun buyurtmalar statistikasini ko'rish. Kunlik, haftalik yoki oylik ma'lumotlar.",
    parameters=[
        OpenApiParameter(
            name='period',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="Statistika davri",
            enum=['today', 'week', 'month'],
            default='today',
            examples=[
                OpenApiExample(name='Bugun', value='today'),
                OpenApiExample(name='Shu hafta', value='week'),
                OpenApiExample(name='Shu oy', value='month'),
            ]
        )
    ],
    responses={
        200: OpenApiResponse(
            response=OrderStatsResponseSerializer,
            description="Statistika ma'lumotlari",
            examples=[
                OpenApiExample(
                    name='Kunlik statistika',
                    value={
                        "summary": {
                            "period": "Bugun",
                            "total_orders": 15,
                            "pending_orders": 3,
                            "in_progress_orders": 8,
                            "completed_orders": 4,
                            "cancelled_orders": 0,
                            "total_baklashka": 150,
                            "total_kuler": 45,
                            "start_date": "2025-11-10T00:00:00Z",
                            "end_date": "2025-11-10T23:59:59Z"
                        },
                        "daily_breakdown": [
                            {
                                "date": "2025-11-10",
                                "total_orders": 15,
                                "completed_orders": 4,
                                "total_baklashka": 150,
                                "total_kuler": 45
                            }
                        ],
                        "generated_at": "2025-11-10T16:30:00Z"
                    }
                )
            ]
        ),
        400: OpenApiResponse(description="Noto'g'ri parametrlar")
    },
    tags=["Statistics"]
)
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def order_statistics(request):
    """
    Buyurtmalar statistikasi endpoint-i
    """
    period = request.query_params.get('period', 'today')
    
    # Davr sanalarini olish
    start_date, end_date, period_name = get_period_dates(period)
    
    # Davr ichidagi buyurtmalarni olish
    orders_queryset = Order.objects.filter(
        created_at__range=[start_date, end_date]
    )
    
    # Asosiy statistika
    summary_stats = calculate_order_stats(
        orders_queryset, period_name, start_date, end_date
    )
    
    # Kunlik taqsimot
    daily_breakdown = get_daily_breakdown(start_date, end_date)
    
    response_data = {
        'summary': summary_stats,
        'daily_breakdown': daily_breakdown,
        'generated_at': timezone.now()
    }
    
    return Response(response_data, status=status.HTTP_200_OK)


@extend_schema(
    summary="Umumiy statistika",
    description="Barcha vaqt uchun umumiy buyurtmalar statistikasi",
    responses={
        200: OpenApiResponse(
            response=OrderStatsSerializer,
            description="Umumiy statistika",
            examples=[
                OpenApiExample(
                    name='Umumiy statistika',
                    value={
                        "period": "Barcha vaqt",
                        "total_orders": 1248,
                        "pending_orders": 25,
                        "in_progress_orders": 47,
                        "completed_orders": 1150,
                        "cancelled_orders": 26,
                        "total_baklashka": 15420,
                        "total_kuler": 4850,
                        "start_date": "2025-01-01T00:00:00Z",
                        "end_date": "2025-11-10T23:59:59Z"
                    }
                )
            ]
        )
    },
    tags=["Statistics"]
)
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def general_statistics(request):
    """
    Umumiy statistika endpoint-i
    """
    # Barcha buyurtmalar
    all_orders = Order.objects.all()
    
    if all_orders.exists():
        first_order = all_orders.order_by('created_at').first()
        start_date = first_order.created_at
    else:
        start_date = timezone.now()
    
    end_date = timezone.now()
    
    # Statistika hisoblash
    stats = calculate_order_stats(
        all_orders, "Barcha vaqt", start_date, end_date
    )
    
    return Response(stats, status=status.HTTP_200_OK)


@extend_schema(
    summary="Eng faol mijozlar",
    description="Belgilangan davr uchun eng ko'p buyurtma bergan mijozlar ro'yxati",
    parameters=[
        OpenApiParameter(
            name='period',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="Statistika davri",
            enum=['today', 'week', 'month', 'all'],
            default='month'
        ),
        OpenApiParameter(
            name='limit',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            description="Natijalar soni",
            default=10
        )
    ],
    responses={
        200: OpenApiResponse(
            response=TopClientsResponseSerializer,
            description="Eng faol mijozlar",
            examples=[
                OpenApiExample(
                    name='Eng faol mijozlar',
                    value={
                        "period": "Shu oy",
                        "top_clients": [
                            {
                                "client_id": 5,
                                "client_name": "Anvar Karimov",
                                "client_phone": "+998901234567",
                                "total_orders": 25,
                                "total_baklashka": 250,
                                "total_kuler": 75,
                                "last_order_date": "2025-11-10T14:30:00Z"
                            }
                        ],
                        "generated_at": "2025-11-10T16:30:00Z"
                    }
                )
            ]
        )
    },
    tags=["Statistics"]
)
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def top_clients(request):
    """
    Eng faol mijozlar statistikasi
    """
    period = request.query_params.get('period', 'month')
    limit = int(request.query_params.get('limit', 10))
    
    # Davr sanalarini olish
    if period == 'all':
        orders_queryset = Order.objects.all()
        period_name = "Barcha vaqt"
    else:
        start_date, end_date, period_name = get_period_dates(period)
        orders_queryset = Order.objects.filter(
            created_at__range=[start_date, end_date]
        )
    
    # Mijozlar bo'yicha guruplash va saralash
    client_stats = orders_queryset.values(
        'client__id',
        'client__full_name', 
        'client__phone_number'
    ).annotate(
        total_orders=Count('id'),
        total_baklashka=Sum('baklashka_soni'),
        total_kuler=Sum('kuler_soni'),
        last_order_date=Max('created_at')
    ).order_by('-total_orders')[:limit]
    
    # Serializer uchun ma'lumotlarni tayyorlash
    top_clients_data = []
    for stat in client_stats:
        top_clients_data.append({
            'client_id': stat['client__id'],
            'client_name': stat['client__full_name'],
            'client_phone': stat['client__phone_number'],
            'total_orders': stat['total_orders'],
            'total_baklashka': stat['total_baklashka'] or 0,
            'total_kuler': stat['total_kuler'] or 0,
            'last_order_date': stat['last_order_date'],
        })
    
    response_data = {
        'period': period_name,
        'top_clients': top_clients_data,
        'generated_at': timezone.now()
    }
    
    return Response(response_data, status=status.HTTP_200_OK)


@extend_schema(
    summary="Kuryerlar statistikasi",
    description="Kuryerlarning ish faoliyati statistikasi",
    parameters=[
        OpenApiParameter(
            name='period',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="Statistika davri",
            enum=['today', 'week', 'month', 'all'],
            default='month'
        )
    ],
    responses={
        200: OpenApiResponse(
            response=CouriersStatsResponseSerializer,
            description="Kuryerlar statistikasi",
            examples=[
                OpenApiExample(
                    name='Kuryerlar statistikasi',
                    value={
                        "period": "Shu oy",
                        "couriers_stats": [
                            {
                                "courier_id": 2,
                                "courier_name": "Bobur Karimov",
                                "courier_username": "bobur_kuryer",
                                "assigned_orders": 45,
                                "completed_orders": 42,
                                "in_progress_orders": 3,
                                "completion_rate": 93.3
                            }
                        ],
                        "generated_at": "2025-11-10T16:30:00Z"
                    }
                )
            ]
        )
    },
    tags=["Statistics"]
)
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def couriers_statistics(request):
    """
    Kuryerlar statistikasi
    """
    period = request.query_params.get('period', 'month')
    
    # Davr sanalarini olish
    if period == 'all':
        orders_queryset = Order.objects.all()
        period_name = "Barcha vaqt"
    else:
        start_date, end_date, period_name = get_period_dates(period)
        orders_queryset = Order.objects.filter(
            created_at__range=[start_date, end_date]
        )
    
    # Kuryerlar ro'yxati
    couriers = User.objects.filter(role='kuryer')
    couriers_stats = []
    
    for courier in couriers:
        # Kuryerga tayinlangan buyurtmalar
        assigned_orders = orders_queryset.filter(assigned_to=courier)
        total_assigned = assigned_orders.count()
        
        if total_assigned > 0:
            completed_orders = assigned_orders.filter(status='completed').count()
            in_progress_orders = assigned_orders.filter(status='in_progress').count()
            completion_rate = (completed_orders / total_assigned) * 100
        else:
            completed_orders = 0
            in_progress_orders = 0
            completion_rate = 0.0
        
        couriers_stats.append({
            'courier_id': courier.id,
            'courier_name': courier.full_name,
            'courier_username': courier.username,
            'assigned_orders': total_assigned,
            'completed_orders': completed_orders,
            'in_progress_orders': in_progress_orders,
            'completion_rate': round(completion_rate, 1)
        })
    
    # Tayinlangan buyurtmalar bo'yicha saralash
    couriers_stats.sort(key=lambda x: x['assigned_orders'], reverse=True)
    
    response_data = {
        'period': period_name,
        'couriers_stats': couriers_stats,
        'generated_at': timezone.now()
    }
    
    return Response(response_data, status=status.HTTP_200_OK)