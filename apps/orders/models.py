from django.db import models
from apps.telegram_users.models import TelegramUsers


class Orders(models.Model):
    user = models.ForeignKey(
        TelegramUsers,
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name="Покупатель"
    )
    shop = models.ForeignKey(
        TelegramUsers,
        on_delete=models.CASCADE,
        related_name="shop_orders",
        verbose_name="Продавец"
    )
    cards = models.JSONField(verbose_name="Список товаров")
    total_sum = models.PositiveIntegerField(verbose_name="Общая сумма", default=0)
    created_at = models.DateTimeField("Дата подачи", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ['-created_at']

    def __str__(self):
        return f"Заказ от {self.user.full_name} у {self.shop.full_name}"
