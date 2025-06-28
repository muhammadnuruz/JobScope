from rest_framework import generics, permissions
from apps.applications.models import Applications
from apps.applications.serializers import ApplicationCreateSerializer
from apps.telegram_users.models import TelegramUsers
from rest_framework.exceptions import ValidationError


class ApplicationCreateAPIView(generics.CreateAPIView):
    queryset = Applications.objects.all()
    serializer_class = ApplicationCreateSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        chat_id = self.request.data.get("chat_id")
        if not chat_id:
            raise ValidationError({"chat_id": "chat_id majburiy."})

        try:
            user = TelegramUsers.objects.get(chat_id=chat_id)
        except TelegramUsers.DoesNotExist:
            raise ValidationError({"chat_id": "Bunday Telegram foydalanuvchisi topilmadi."})

        serializer.save(user=user)
