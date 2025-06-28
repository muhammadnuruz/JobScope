from rest_framework import serializers
from apps.applications.models import Applications
from apps.companies.models import Companies


class ApplicationCreateSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(
        queryset=Companies.objects.all(),
        required=True
    )

    class Meta:
        model = Applications
        fields = ['company', 'amount_requested']

    def validate_amount_requested(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Поле 'Сумма' обязательно для заполнения.")
        if not value.replace(" ", "").isdigit():
            raise serializers.ValidationError("Сумма должна содержать только цифры.")
        return value.strip()
