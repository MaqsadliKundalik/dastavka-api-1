from django.urls import path
from . import views

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
]