from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.companies.views import CompanyViewSet, CompanyDetailViewSet

router = DefaultRouter()
router.register(r'companies', CompanyViewSet, basename='company')

urlpatterns = [
    path('', include(router.urls)),
    path('companies/<int:pk>/', CompanyDetailViewSet.as_view(), name='company-detail'),
]
