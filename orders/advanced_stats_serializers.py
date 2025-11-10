from rest_framework import serializers


class TopClientSerializer(serializers.Serializer):
    """
    Eng faol mijozlar uchun serializer
    """
    client_id = serializers.IntegerField(read_only=True, help_text="Mijoz ID")
    client_name = serializers.CharField(read_only=True, help_text="Mijoz ismi")
    client_phone = serializers.CharField(read_only=True, help_text="Mijoz telefoni")
    total_orders = serializers.IntegerField(read_only=True, help_text="Jami buyurtmalar soni")
    total_baklashka = serializers.IntegerField(read_only=True, help_text="Jami baklashkalar soni")
    total_kuler = serializers.IntegerField(read_only=True, help_text="Jami kulerlar soni")
    last_order_date = serializers.DateTimeField(read_only=True, help_text="Oxirgi buyurtma sanasi")


class CourierStatsSerializer(serializers.Serializer):
    """
    Kuryer statistikasi uchun serializer
    """
    courier_id = serializers.IntegerField(read_only=True, help_text="Kuryer ID")
    courier_name = serializers.CharField(read_only=True, help_text="Kuryer ismi")
    courier_username = serializers.CharField(read_only=True, help_text="Kuryer username")
    assigned_orders = serializers.IntegerField(read_only=True, help_text="Tayinlangan buyurtmalar")
    completed_orders = serializers.IntegerField(read_only=True, help_text="Yakunlangan buyurtmalar")
    in_progress_orders = serializers.IntegerField(read_only=True, help_text="Jarayondagi buyurtmalar")
    completion_rate = serializers.FloatField(read_only=True, help_text="Yakunlash foizi")


class TopClientsResponseSerializer(serializers.Serializer):
    """
    Eng faol mijozlar javob serializer
    """
    period = serializers.CharField(read_only=True, help_text="Davr")
    top_clients = TopClientSerializer(many=True, read_only=True, help_text="Eng faol mijozlar")
    generated_at = serializers.DateTimeField(read_only=True, help_text="Yaratilgan vaqt")


class CouriersStatsResponseSerializer(serializers.Serializer):
    """
    Kuryerlar statistikasi javob serializer
    """
    period = serializers.CharField(read_only=True, help_text="Davr")
    couriers_stats = CourierStatsSerializer(many=True, read_only=True, help_text="Kuryerlar statistikasi")
    generated_at = serializers.DateTimeField(read_only=True, help_text="Yaratilgan vaqt")