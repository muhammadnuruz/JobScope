from rest_framework import viewsets, filters
from rest_framework.generics import RetrieveAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny

from apps.companies.models import Companies
from apps.companies.serializers import CompaniesSerializer


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Companies.objects.all()
    serializer_class = CompaniesSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    permission_classes = [AllowAny]


# class CompanyDetailViewSet(RetrieveAPIView):
#     queryset = Companies.objects.all()
#     serializer_class = CompaniesSerializer
#     permission_classes = [AllowAny]


class CompanyDetailViewSet(RetrieveUpdateAPIView):
    queryset = Companies.objects.all()
    serializer_class = CompaniesSerializer
    permission_classes = [AllowAny]
