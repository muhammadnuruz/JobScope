from django.contrib import admin
from .models import Cards


@admin.register(Cards)
class CardsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'price', 'image_file_id', 'created_at')
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('name', 'user__id', 'user_full_name')
    list_filter = ('created_at',)
    fields = ('user', 'imageUrl', 'name', 'price', 'created_at', 'updated_at')
    ordering = ('-created_at',)

    def image_file_id(self, obj):
        return obj.imageUrl

    image_file_id.short_description = "Telegram file_id"
