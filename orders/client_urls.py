from django.urls import path
from .client_views import (
    ClientListCreateView,
    ClientDetailView,
    client_orders,
    clients_stats
)

urlpatterns = [
    # Mijozlar CRUD
    path('', ClientListCreateView.as_view(), name='client-list-create'),
    path('<int:pk>/', ClientDetailView.as_view(), name='client-detail'),
    
    # Mijoz buyurtmalari
    path('<int:pk>/orders/', client_orders, name='client-orders'),
    
    # Mijozlar statistikasi
    path('stats/', clients_stats, name='clients-stats'),
]