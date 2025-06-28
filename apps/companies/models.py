from django.db import models


class Companies(models.Model):
    name = models.CharField("Название компании", max_length=255)
    description = models.TextField("Описание", blank=True, null=True)
    link = models.CharField("Линк", blank=True, null=True)
    group_id = models.CharField("Групповой идентификатор", max_length=50)
    is_approved = models.BooleanField("Одобрено админом", default=False)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)
    managers = models.ManyToManyField(
        "telegram_users.TelegramUsers",
        related_name='managed_companies',
        blank=True,
        verbose_name="Менеджеры"
    )
    employees = models.ManyToManyField(
        "telegram_users.TelegramUsers",
        related_name='worked_companies',
        blank=True,
        verbose_name="Сотрудники"
    )

    class Meta:
        verbose_name = "Компания"
        verbose_name_plural = "Компании"

    def __str__(self):
        return self.name
