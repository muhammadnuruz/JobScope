from rest_framework import serializers

from apps.companies.models import Companies
from apps.telegram_users.models import TelegramUsers


class TelegramUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramUsers
        fields = "__all__"


class TelegramUsersCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramUsers
        exclude = ['created_at', 'updated_at', 'status', 'favourite_companies', ]


class EmployeeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramUsers
        fields = "__all__"


class NearbyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramUsers
        fields = "__all__"


class AddFavouriteCompanySerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset=TelegramUsers.objects.all())
    company = serializers.PrimaryKeyRelatedField(queryset=Companies.objects.all())

    def validate(self, data):
        user = data['user']
        company = data['company']
        if user.favourite_companies.filter(id=company.id).exists():
            raise serializers.ValidationError("Компания уже в избранном.")
        return data
