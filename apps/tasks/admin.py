from django.contrib import admin
from django.utils.html import format_html
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'user_link', 'company_link', 'status_colored', 'deadline',
        'reward', 'penalty', 'completed_at', 'created_at'
    )
    list_filter = ('status', 'deadline', 'created_at', 'company')
    search_fields = (
        'title',
        'description',
        'user__full_name',
        'user__username',
        'user__phone_number',
        'company__name'
    )
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at', 'status_colored', 'user_link', 'company_link')

    fieldsets = (
        ('📌 Основная информация', {
            'fields': (
                'title',
                'description',
                'user',
                'company',
                'user_link',
                'company_link',
                'status',
                'status_colored'
            )
        }),
        ('📆 Сроки выполнения', {
            'fields': ('deadline', 'completed_at')
        }),
        ('🎯 Баллы', {
            'fields': ('reward', 'penalty')
        }),
        ('🕓 Системные метки', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def user_link(self, obj):
        if obj.user:
            return format_html(
                '<a href="/admin/telegram_users/telegramusers/{}/change/" target="_blank">{}</a>',
                obj.user.id,
                obj.user.full_name or obj.user.username or obj.user.chat_id
            )
        return "-"

    user_link.short_description = "Сотрудник"

    def company_link(self, obj):
        if obj.company:
            return format_html(
                '<a href="/admin/companies/companies/{}/change/" target="_blank">{}</a>',
                obj.company.id,
                obj.company.name
            )
        return "-"

    company_link.short_description = "Компания"

    def status_colored(self, obj):
        emoji = {
            'in_progress': '🟠 В процессе',
            'late': '🔴 Просрочен',
            'completed': '✅ Завершено',
        }.get(obj.status, obj.status)
        return format_html('<span>{}</span>', emoji)

    status_colored.short_description = "Статус"
