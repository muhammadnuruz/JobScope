from django.db import models

from apps.companies.models import Companies


class TelegramUsers(models.Model):
    STATUS_CHOICES = [
        ('user', 'Пользователь'),
        ('customer', 'Seller'),
        ('employee', 'Сотрудник'),
        ('manager', 'Менеджер'),
    ]

    chat_id = models.BigIntegerField("Telegram Chat ID", unique=True)
    username = models.CharField("Юзернейм", max_length=150, blank=True, null=True)
    full_name = models.CharField("Полное имя", max_length=255, blank=True, null=True)
    phone_number = models.CharField("Номер телефона", max_length=20, blank=True, null=True)
    location_lat = models.FloatField("Широта", blank=True, null=True)
    location_lng = models.FloatField("Долгота", blank=True, null=True)
    photo = models.ImageField("Фото профиля", upload_to='telegram_users/photos/', blank=True, null=True)
    point = models.IntegerField("Награда", default=0, blank=True)
    fine = models.IntegerField("Штраф", default=0, blank=True)
    status = models.CharField("Статус", max_length=10, default="user", choices=STATUS_CHOICES)
    favourite_companies = models.ManyToManyField(
        Companies,
        blank=True,
        related_name='favourited_by_users',
        verbose_name="Избранные компании"
    )
    created_at = models.DateTimeField("Создан", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлен", auto_now=True)

    class Meta:
        verbose_name = "Telegram-пользователь"
        verbose_name_plural = "Telegram-пользователи"

    def __str__(self):
        return f"{self.full_name or self.username or self.chat_id}"
