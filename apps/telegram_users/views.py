from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import RetrieveAPIView, CreateAPIView, UpdateAPIView, ListAPIView
from apps.telegram_users.serializers import TelegramUsersSerializer, TelegramUsersCreateSerializer, \
    AddFavouriteCompanySerializer
from apps.companies.models import Companies
from math import radians, cos, sin, asin, sqrt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from apps.telegram_users.serializers import EmployeeListSerializer
from apps.telegram_users.models import TelegramUsers
from apps.telegram_users.serializers import NearbyUserSerializer


class TelegramUsersListViewSet(ListAPIView):
    queryset = TelegramUsers.objects.all()
    serializer_class = TelegramUsersSerializer
    permission_classes = [AllowAny]


class TelegramUsersCreateViewSet(CreateAPIView):
    queryset = TelegramUsers.objects.all()
    serializer_class = TelegramUsersCreateSerializer
    permission_classes = [AllowAny]


class TelegramUsersUpdateViewSet(UpdateAPIView):
    queryset = TelegramUsers.objects.all()
    serializer_class = TelegramUsersCreateSerializer
    permission_classes = [AllowAny]


class TelegramUsersChatIdDetailViewSet(RetrieveAPIView):
    queryset = TelegramUsers.objects.all()
    serializer_class = TelegramUsersSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        chat_id = self.kwargs.get('chat_id')
        return get_object_or_404(TelegramUsers, chat_id=chat_id)


class TelegramUsersDetailViewSet(RetrieveAPIView):
    queryset = TelegramUsers.objects.all()
    serializer_class = TelegramUsersSerializer
    permission_classes = [AllowAny]


class EmployeesByCompanyView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, company_id):
        employees = TelegramUsers.objects.filter(
            status='employee',
            worked_companies__id=company_id
        )
        serializer = EmployeeListSerializer(employees, many=True)
        return Response(serializer.data)


def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    return R * c


class NearbyUsersView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        lat = request.query_params.get('lat')
        lng = request.query_params.get('lng')
        if not lat or not lng:
            return Response({"detail": "Koordinatalar (lat, lng) yuborilishi kerak."}, status=400)
        try:
            lat, lng = float(lat), float(lng)
        except ValueError:
            return Response({"detail": "Koordinatalar noto‘g‘ri formatda."}, status=400)
        all_users = TelegramUsers.objects.filter(status='customer') \
            .exclude(location_lat__isnull=True) \
            .exclude(location_lng__isnull=True)
        nearby = []
        for user in all_users:
            distance = haversine(lat, lng, user.location_lat, user.location_lng)
            if distance <= 6:
                nearby.append(user)
        serializer = NearbyUserSerializer(nearby, many=True)
        return Response(serializer.data)


class UserEmployeeCompaniesAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, chat_id):
        try:
            user = TelegramUsers.objects.get(chat_id=chat_id)
        except TelegramUsers.DoesNotExist:
            return Response({"detail": "Foydalanuvchi topilmadi."}, status=404)

        if user.status != "employee":
            return Response({"detail": "Foydalanuvchi xodim emas."}, status=400)

        companies = Companies.objects.filter(employees=user)
        data = [{"id": company.id, "name": company.name} for company in companies]
        return Response(data, status=200)


class UserManagerCompaniesAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, chat_id):
        try:
            user = TelegramUsers.objects.get(chat_id=chat_id)
        except TelegramUsers.DoesNotExist:
            return Response({"detail": "Foydalanuvchi topilmadi."}, status=404)

        if user.status != "manager":
            return Response({"detail": "Foydalanuvchi menejer emas."}, status=400)

        companies = Companies.objects.filter(managers=user)
        data = [{"id": company.id, "name": company.name} for company in companies]
        return Response(data, status=200)


class AddFavouriteCompanyAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = AddFavouriteCompanySerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            company = serializer.validated_data['company']
            user.favourite_companies.add(company)
            return Response({"detail": "Компания добавлена в избранное."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        serializer = AddFavouriteCompanySerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            company = serializer.validated_data['company']

            user.favourite_companies.remove(company)
            return Response({"detail": "Компания удалена из избранного."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
