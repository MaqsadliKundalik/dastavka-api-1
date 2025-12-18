import django_filters
from .models import Order, Client


class OrderFilter(django_filters.FilterSet):
    """
    Buyurtmalar uchun murakkab filterlash
    """
    
    # Client ID bo'yicha faqat to'liq moslikda qidirish
    client_id = django_filters.NumberFilter(field_name='client__id')
    
    # Client nomi bo'yicha qidirish
    client_name = django_filters.CharFilter(field_name='client__full_name', lookup_expr='icontains')
    
    # Client telefon raqami bo'yicha qidirish
    client_phone = django_filters.CharFilter(field_name='client__phone_number', lookup_expr='icontains')
    
    # Arenda mavjud bo'lgan buyurtmalarni filterlash
    has_arenda = django_filters.BooleanFilter(method='filter_has_arenda')
    
    class Meta:
        model = Order
        fields = ['status', 'assigned_to', 'created_by']
    
    def filter_has_arenda(self, queryset, name, value):
        """
        Arenda mavjud bo'lgan buyurtmalarni filterlash
        has_arenda=true -> arenda_soni > 0 bo'lgan orderlar
        has_arenda=false -> arenda_soni = 0 bo'lgan orderlar
        """
        if value is True:
            return queryset.filter(arenda_soni__gt=0)
        elif value is False:
            return queryset.filter(arenda_soni=0)
        return queryset


class ClientFilter(django_filters.FilterSet):
    """
    Mijozlar uchun filterlash
    """
    
    # Client ID bo'yicha qidirish (to'liq ID yoki qismiy)
    id = django_filters.CharFilter(method='filter_client_id')
    
    class Meta:
        model = Client
        fields = ['id']
    
    def filter_client_id(self, queryset, name, value):
        """
        Client ID bo'yicha filterlash - to'liq ID yoki qismiy ID qidirish
        Masalan: ID=12345 bo'lsa, '123' kiritganda ham topadi
        """
        if value:
            # ID'si qismiy mos keluvchi clientlarni qidirish
            return queryset.filter(id__icontains=value)
        return queryset