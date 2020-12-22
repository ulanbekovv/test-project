from rest_framework import serializers
from .models import Product, Stock


class ProductSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(read_only=True, format='%d.%m.%Y %C:%M')
    class Meta:
        model = Product
        fields = ('phone_number', 'name', 'total_bonus', 'card_number', 'id', 'count', 'date')