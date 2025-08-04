from django.db import models

from apps.telegram_users.models import TelegramUsers


class Cards(models.Model):
    user = models.ForeignKey(
        TelegramUsers,
        on_delete=models.CASCADE,
        verbose_name="Telegram-пользователь"
    )
    imageUrl = models.CharField("Ссылка на изображение", max_length=255)
    name = models.CharField("Имя", max_length=255)
    price = models.IntegerField("Цена")
    created_at = models.DateTimeField("Дата подачи", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)

    class Meta:
        verbose_name = "Карта"
        verbose_name_plural = "Карты"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.price}"
