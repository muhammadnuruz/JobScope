from aiogram.types import CallbackQuery

from bot.config import get_card_by_id, get_user_by_chat_id, save_basket_to_db, get_baskets, create_order_from_basket, \
    clear_basket
from bot.dispatcher import dp


@dp.callback_query_handler(lambda c: c.data.startswith("plus_"))
async def ordering_function(call: CallbackQuery):
    tg_user = await get_user_by_chat_id(call.from_user.id)
    if tg_user:
        _, num, id_ = call.data.split("_")
        card = await get_card_by_id(id_=id_)
        basket = await save_basket_to_db(shop_id=card.user.id, user_id=tg_user.id, card_id=card.id, count=int(num))
        await call.answer(
            f"🧺 {num} товаров добавлено в корзину.\n"
            f"📦 Всего в корзине: {basket.count} товаров.",
            show_alert=True
        )
    else:
        await call.answer(f"⛔ Сначала зарегистрируйтесь у бота.\n\n👉 t.me/TujjorSBot", show_alert=True)


def format_order_message(order) -> str:
    lines = [f"🧾 Заказ от: {order.user.full_name}"]
    lines.append(f"👤 Номер телефона продавца: {order.shop.phone_number}")
    lines.append(f"👤 Клиент телефона продавца: {order.user.phone_number}")
    lines.append(f"🛍 Продавец: {order.shop.full_name}")
    lines.append("\n📦 Товары:")

    for idx, item in enumerate(order.cards, start=1):
        lines.append(
            f"{idx}. {item['name']} — {item['count']} шт. × {item['price']} сум = {item['count'] * item['price']} сум"
        )

    lines.append(f"\n💰 Общая сумма: {order.total_sum} сум")
    lines.append(f"📅 Дата: {order.created_at.strftime('%d.%m.%Y %H:%M')}")

    return "\n".join(lines)


@dp.callback_query_handler(lambda c: c.data.startswith("close_order_"))
async def ordering_function_2(call: CallbackQuery):
    tg_user = await get_user_by_chat_id(call.from_user.id)
    if not tg_user:
        await call.answer(
            "⛔ Сначала зарегистрируйтесь у бота.\n\n👉 t.me/TujjorSBot",
            show_alert=True
        )
        return

    id_ = call.data.split("_")[-1]
    card = await get_card_by_id(id_=id_)
    if not card:
        await call.answer("⛔ Карточка не найдена.", show_alert=True)
        return

    shop = card.user
    order = await create_order_from_basket(user=tg_user, shop=shop)

    if not order:
        await call.answer("⛔ Ваша корзина пуста.", show_alert=True)
        return

    text = format_order_message(order)

    await call.bot.send_message(chat_id=call.from_user.id, text=f"✅ Ваш заказ успешно оформлен!\n\n" + text)

    try:
        await call.bot.send_message(chat_id=shop.chat_id, text=f"🆕 Новый заказ!\n\n{text}")
    except Exception:
        pass


@dp.callback_query_handler(lambda c: c.data.startswith("clear_basket_"))
async def clear_basket_function(call: CallbackQuery):
    tg_user = await get_user_by_chat_id(call.from_user.id)
    if tg_user:
        await clear_basket(tg_user.id)
        await call.answer("🗑 Корзина успешно очищена!", show_alert=True)
    else:
        await call.answer("⛔ Сначала зарегистрируйтесь у бота.\n\n👉 t.me/TujjorSBot", show_alert=True)
