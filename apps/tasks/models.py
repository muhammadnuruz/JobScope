from django.db import models

from apps.companies.models import Companies
from apps.telegram_users.models import TelegramUsers


class Task(models.Model):
    STATUS_CHOICES = [
        ('in_progress', '🟠 В процессе'),
        ('late', '🔴 Просрочен'),
        ('done', 'Завершено'),
    ]

    user = models.ForeignKey(
        TelegramUsers,
        on_delete=models.CASCADE,
        related_name='tasks',
        verbose_name='Сотрудник'
    )
    company = models.ForeignKey(
        Companies,
        on_delete=models.CASCADE,
        related_name="tasks",
        verbose_name="Компания"
    )
    title = models.CharField("Название задачи", max_length=255)
    description = models.TextField("Описание", blank=True, null=True)
    deadline = models.DateField("Крайний срок")
    completed_at = models.DateTimeField("Время выполнения", blank=True, null=True)
    reward = models.IntegerField("Награда (баллы)", default=0)
    penalty = models.IntegerField("Штраф (баллы)", default=0)
    status = models.CharField("Статус", max_length=20, choices=STATUS_CHOICES, default='in_pogress')
    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} — {self.user}"
