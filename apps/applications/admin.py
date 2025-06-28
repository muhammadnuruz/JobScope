from django.contrib import admin
from apps.applications.models import Applications


@admin.register(Applications)
class ApplicationsAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user_display', 'company', 'amount_requested',
        'created_at', 'updated_at'
    )
    list_filter = ('created_at', 'company')
    search_fields = (
        'user__full_name',
        'user__phone_number',
        'company__name',
        'amount_requested',
    )
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

    fieldsets = (
        ('📌 Основная информация', {
            'fields': ('user', 'company', 'amount_requested')
        }),
        ('⏱️ Временные метки', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def user_display(self, obj):
        return f"{obj.user.full_name or obj.user.username or obj.user.chat_id}"

    user_display.short_description = "Пользователь"
