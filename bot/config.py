import os
from typing import Optional

import django
from asgiref.sync import sync_to_async
from datetime import timedelta, datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'JobScope.settings')
django.setup()

from apps.basket.models import Basket
from apps.telegram_users.models import TelegramUsers
from apps.cards.models import Cards


@sync_to_async
def get_telegram_users():
    return list(TelegramUsers.objects.only('chat_id'))


@sync_to_async
def get_user_by_chat_id(chat_id: int):
    try:
        return TelegramUsers.objects.get(chat_id=chat_id)
    except Exception:
        return None


@sync_to_async
def get_user_by_id(_id: int):
    try:
        return TelegramUsers.objects.get(id=_id)
    except Exception:
        return None


@sync_to_async
def create_user_by_chat_id(chat_id: int,
                           full_name: str,
                           username: str) -> TelegramUsers:
    try:
        user, created = TelegramUsers.objects.get_or_create(
            chat_id=chat_id,
            defaults={
                "full_name": full_name,
                "username": username,
            }
        )
        return user
    except Exception:
        return None


@sync_to_async
def update_user_by_chat_id(
        chat_id: int,
        full_name: str = None,
        username: str = None,
        is_vip: bool = None) -> TelegramUsers | None:
    try:
        user = TelegramUsers.objects.get(chat_id=chat_id)
        if full_name is not None:
            user.full_name = full_name
        if username is not None:
            user.username = username
        if is_vip is not None:
            user.is_vip = is_vip
        user.save()
        return user
    except Exception:
        return None


@sync_to_async
def check_subscription_function(chat_id: int) -> bool:
    try:
        tg_user = TelegramUsers.objects.get(chat_id=chat_id)
        if tg_user.is_vip:
            now = datetime.now(tz=tg_user.updated_at.tzinfo)
            if now - tg_user.updated_at <= timedelta(days=30):
                return True
        return False
    except Exception:
        return False


@sync_to_async
def get_all_cards(chat_id: int) -> list:
    return list(Cards.objects.filter(user__chat_id=chat_id))


@sync_to_async
def get_card_by_id(id_: int) -> Cards | None:
    try:
        return Cards.objects.select_related("user").get(id=id_)
    except Cards.DoesNotExist:
        return None


@sync_to_async
def delete_card_by_id(id_: int) -> bool:
    try:
        card = Cards.objects.get(id=id_)
        card.delete()
        return True
    except Cards.DoesNotExist:
        return False


@sync_to_async
def save_card_to_db(chat_id: int, imageUrl: str, name: str, price: int):
    try:
        user = TelegramUsers.objects.get(chat_id=chat_id)
        Cards.objects.create(
            user=user,
            imageUrl=imageUrl,
            name=name,
            price=price
        )
    except TelegramUsers.DoesNotExist:
        pass


@sync_to_async
def save_basket_to_db(shop_id: int, user_id: int, card_id: int, count: int):
    try:
        basket, created = Basket.objects.get_or_create(
            shop_id=shop_id,
            user_id=user_id,
            card_id=card_id,
            defaults={'count': count}
        )
        if not created:
            basket.count += count
            basket.save()
    except Exception as e:
        pass


@sync_to_async
def get_baskets(shop_id: int, user_id: int):
    return list(
        Basket.objects.select_related("user", "shop", "card")
        .filter(shop_id=shop_id, user_id=user_id)
    )
