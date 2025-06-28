from rest_framework import serializers

from apps.companies.models import Companies


class CompaniesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Companies
        fields = "__all__"
