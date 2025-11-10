from rest_framework import serializers
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Order


class OrderStatsSerializer(serializers.Serializer):
    """
    Buyurtmalar statistikasi uchun serializer
    """
    period = serializers.CharField(read_only=True, help_text="Davr nomi")
    total_orders = serializers.IntegerField(read_only=True, help_text="Jami buyurtmalar soni")
    pending_orders = serializers.IntegerField(read_only=True, help_text="Kutilayotgan buyurtmalar")
    in_progress_orders = serializers.IntegerField(read_only=True, help_text="Jarayonda bo'lgan buyurtmalar")
    completed_orders = serializers.IntegerField(read_only=True, help_text="Yakunlangan buyurtmalar")
    cancelled_orders = serializers.IntegerField(read_only=True, help_text="Bekor qilingan buyurtmalar")
    total_baklashka = serializers.IntegerField(read_only=True, help_text="Jami baklashkalar soni")
    total_kuler = serializers.IntegerField(read_only=True, help_text="Jami kulerlar soni")
    start_date = serializers.DateTimeField(read_only=True, help_text="Davr boshlanish sanasi")
    end_date = serializers.DateTimeField(read_only=True, help_text="Davr tugash sanasi")


class DailyStatsSerializer(serializers.Serializer):
    """
    Kunlik statistika uchun serializer
    """
    date = serializers.DateField(read_only=True, help_text="Sana")
    total_orders = serializers.IntegerField(read_only=True, help_text="Kun davomida yaratilgan buyurtmalar")
    completed_orders = serializers.IntegerField(read_only=True, help_text="Kun davomida yakunlangan buyurtmalar")
    total_baklashka = serializers.IntegerField(read_only=True, help_text="Kun davomida jami baklashkalar")
    total_kuler = serializers.IntegerField(read_only=True, help_text="Kun davomida jami kulerlar")


class OrderStatsResponseSerializer(serializers.Serializer):
    """
    Statistika javob uchun asosiy serializer
    """
    summary = OrderStatsSerializer(read_only=True, help_text="Umumiy statistika")
    daily_breakdown = DailyStatsSerializer(many=True, read_only=True, help_text="Kunlik taqsimot")
    generated_at = serializers.DateTimeField(read_only=True, help_text="Hisobot yaratilgan vaqt")