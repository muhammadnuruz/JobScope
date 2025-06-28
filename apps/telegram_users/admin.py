from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import TelegramUsers


@admin.register(TelegramUsers)
class TelegramUsersAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'full_name_display', 'username', 'phone_number',
        'status', 'point', 'fine',
        'has_location', 'created_at'
    )
    list_filter = ('status', 'created_at')
    search_fields = ('full_name', 'username', 'phone_number', 'chat_id')
    readonly_fields = ('created_at', 'updated_at', 'chat_id', 'photo_preview')
    ordering = ('-created_at',)
    filter_horizontal = ('favourite_companies',)

    fieldsets = (
        ('🔹 Telegram аккаунт', {
            'fields': ('chat_id', 'username', 'full_name', 'phone_number')
        }),
        ('🧑‍💼 Роль и статус', {
            'fields': ('status',)
        }),
        ('📍 Геолокация', {
            'fields': ('location_lat', 'location_lng')
        }),
        ('🎯 Баллы и штрафы', {
            'fields': ('point', 'fine')
        }),
        ('🖼️ Фото', {
            'fields': ('photo', 'photo_preview')
        }),
        ('❤️ Избранные компании', {
            'fields': ('favourite_companies',)
        }),
        ('⏱️ Временные метки', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def full_name_display(self, obj):
        return obj.full_name or '—'
    full_name_display.short_description = "Полное имя"

    def has_location(self, obj):
        return bool(obj.location_lat and obj.location_lng)
    has_location.boolean = True
    has_location.short_description = "Локация?"

    def photo_preview(self, obj):
        if obj.photo:
            return mark_safe(
                f'<img src="{obj.photo.url}" width="100" height="100" style="object-fit: cover; border-radius: 10px;" />'
            )
        return "Нет фото"
    photo_preview.short_description = "Превью"
