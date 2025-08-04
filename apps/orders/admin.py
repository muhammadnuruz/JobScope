from django.contrib import admin
from django.utils.html import format_html, format_html_join
from django.utils.safestring import mark_safe
from .models import Orders


@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user_info',
        'shop_info',
        'total_sum',
        'created_at',
    )
    search_fields = (
        'user__telegram_id',
        'user__full_name',
        'shop__telegram_id',
        'shop__full_name',
    )
    list_filter = ('created_at',)
    ordering = ('-created_at',)
    readonly_fields = ('user', 'shop', 'cards_pretty', 'total_sum', 'created_at', 'updated_at')
    fields = ('user', 'shop', 'cards_pretty', 'total_sum', 'created_at', 'updated_at')

    def user_info(self, obj):
        return f"{obj.user.full_name} ({obj.user.telegram_id})"

    user_info.short_description = "Покупатель"

    def shop_info(self, obj):
        return f"{obj.shop.full_name} ({obj.shop.telegram_id})"

    shop_info.short_description = "Продавец"

    def cards_pretty(self, obj):
        if not obj.cards:
            return "—"
        rows = format_html_join(
            '\n',
            "<li><b>{}</b> — {} шт. × {} сум = <code>{}</code> сум</li>",
            (
                (
                    card.get("name", "❓"),
                    card.get("count", 0),
                    card.get("price", 0),
                    card.get("count", 0) * card.get("price", 0)
                )
                for card in obj.cards
            )
        )
        return mark_safe(f"<ul>{rows}</ul>")

    cards_pretty.short_description = "Список товаров"
