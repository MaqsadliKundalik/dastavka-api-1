from django.urls import path
from . import views, stats_views

app_name = 'orders'

urlpatterns = [
    # CRUD operatsiyalar
    path('', views.OrderListCreateView.as_view(), name='order-list-create'),
    path('<int:pk>/', views.OrderDetailView.as_view(), name='order-detail'),
    
    # Status va kuryer tayinlash
    path('<int:pk>/status/', views.update_order_status, name='update-order-status'),
    path('<int:pk>/assign/', views.assign_courier, name='assign-courier'),
    
    # Shaxsiy buyurtmalar
    path('my/', views.my_orders, name='my-orders'),
    
    # Statistika
    path('stats/', stats_views.order_statistics, name='order-statistics'),
    path('stats/general/', stats_views.general_statistics, name='general-statistics'),
    path('stats/top-clients/', stats_views.top_clients, name='top-clients'),
    path('stats/couriers/', stats_views.couriers_statistics, name='couriers-statistics'),
]