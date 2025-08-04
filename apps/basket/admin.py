from django.contrib import admin
from .models import Basket


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user_full_name',
        'shop_full_name',
        'card_name',
        'count',
        'created_at',
        'updated_at',
    )

    list_filter = ('created_at', 'updated_at')
    search_fields = (
        'user__chat_id',
        'user__full_name',
        'shop__chat_id',
        'shop__full_name',
        'card__name',
    )
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

    autocomplete_fields = ('user', 'shop', 'card')
    list_select_related = ('user', 'shop', 'card')

    def user_full_name(self, obj):
        return obj.user.full_name

    user_full_name.short_description = "Покупатель"

    def shop_full_name(self, obj):
        return obj.shop.full_name

    shop_full_name.short_description = "Продавец"

    def card_name(self, obj):
        return obj.card.name

    card_name.short_description = "Карта"
