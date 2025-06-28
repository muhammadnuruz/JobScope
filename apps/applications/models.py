from django.db import models
from apps.telegram_users.models import TelegramUsers
from apps.companies.models import Companies


class Applications(models.Model):
    user = models.ForeignKey(
        TelegramUsers,
        on_delete=models.CASCADE,
        verbose_name="Telegram-пользователь"
    )
    company = models.ForeignKey(
        Companies,
        on_delete=models.CASCADE,
        verbose_name="Компания"
    )

    amount_requested = models.CharField("Запрашиваемая сумма", blank=True)
    created_at = models.DateTimeField("Дата подачи", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} → {self.company.name}"
