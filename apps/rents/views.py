from rest_framework import generics, permissions

from rest_framework import serializers
from .models import Debt
from .serializers import DebtCreateSerializer, DebtListSerializer
from ..telegram_users.models import TelegramUsers


class DebtCreateView(generics.CreateAPIView):
    queryset = Debt.objects.all()
    serializer_class = DebtCreateSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        chat_id = self.request.data.get("chat_id")
        if not chat_id:
            raise serializers.ValidationError({"chat_id": "chat_id yuborilishi kerak"})

        try:
            telegram_user = TelegramUsers.objects.get(chat_id=chat_id)
        except TelegramUsers.DoesNotExist:
            raise serializers.ValidationError({"chat_id": "Telegram foydalanuvchisi topilmadi"})

        serializer.save(user=telegram_user)


class DebtListView(generics.ListAPIView):
    serializer_class = DebtListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        chat_id = self.request.query_params.get("chat_id")
        if not chat_id:
            return Debt.objects.none()

        try:
            telegram_user = TelegramUsers.objects.get(chat_id=chat_id)
            return Debt.objects.filter(user=telegram_user).order_by('deadline')
        except TelegramUsers.DoesNotExist:
            return Debt.objects.none()


class DebtDeleteAPIView(generics.DestroyAPIView):
    queryset = Debt.objects.all()
    permission_classes = [permissions.AllowAny]
