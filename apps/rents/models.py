from django.db import models
from apps.telegram_users.models import TelegramUsers


class Debt(models.Model):
    user = models.ForeignKey(
        TelegramUsers,
        on_delete=models.CASCADE,
        related_name='debts',
        verbose_name='Пользователь'
    )
    borrower_name = models.CharField("Имя должника", max_length=255)
    amount = models.IntegerField("Сумма долга (сум)")
    deadline = models.DateField("Срок возврата")
    price = models.IntegerField()
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)

    class Meta:
        verbose_name = "Долг"
        verbose_name_plural = "Долги"
        ordering = ['deadline']

    def __str__(self):
        return f"{self.borrower_name} — {self.amount} сум"
