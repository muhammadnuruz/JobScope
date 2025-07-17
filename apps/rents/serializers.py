from rest_framework import serializers
from .models import Debt


class DebtCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Debt
        fields = ['id', 'borrower_name', 'amount', 'deadline', 'user', 'price']
        read_only_fields = ['user']


class DebtListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Debt
        fields = ['id', 'borrower_name', 'amount', 'deadline', 'price', 'created_at']
