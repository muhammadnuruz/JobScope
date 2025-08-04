from django.db import models

from apps.telegram_users.models import TelegramUsers
from apps.cards.models import Cards


class Basket(models.Model):
    shop = models.ForeignKey(
        TelegramUsers,
        on_delete=models.CASCADE,
        related_name="shop_baskets",
        verbose_name="Продавец"
    )
    user = models.ForeignKey(
        TelegramUsers,
        on_delete=models.CASCADE,
        related_name="customer_baskets",
        verbose_name="Telegram-пользователь"
    )
    card = models.ForeignKey(
        Cards,
        on_delete=models.CASCADE,
        verbose_name="Карта"
    )
    count = models.IntegerField(verbose_name="Число")
    created_at = models.DateTimeField("Дата подачи", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"
        ordering = ['-shop__id']

    def __str__(self):
        return f"{self.user} - {self.card}"
