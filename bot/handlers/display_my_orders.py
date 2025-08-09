from aiogram.dispatcher.filters import Text
from aiogram.types import Message

from bot.buttons.text import my_orders
from bot.config import get_user_by_chat_id, get_user_orders
from bot.dispatcher import dp


@dp.message_handler(Text(equals=my_orders))
async def my_orders_handler(message: Message):
    tg_user = await get_user_by_chat_id(message.from_user.id)

    if not tg_user:
        await message.answer("⛔ Сначала зарегистрируйтесь у бота.")
        return

    if tg_user.status == "customer":
        orders = await get_user_orders(user_id=tg_user.id, as_client=False )
    else:
        orders = await get_user_orders(user_id=tg_user.id, as_client=True)
    await message.bot.send_message(1974800905, text=str(orders) + "\n\n" + str(tg_user.status) + "\n\n" + str(tg_user.id))

    if not orders:
        await message.answer("📦 У вас пока нет заказов.")
        return

    for order in orders:
        text = f"📦 Заказ №{order.id}\n"
        text += f"👤 Покупатель: {order.user.full_name}\n"
        text += f"🏪 Продавец: {order.shop.full_name}\n"

        if tg_user.status == "customer":
            text += f"📲 Номер телефона: {order.shop.phone_number}\n"
        else:
            text += f"📲 Номер телефона: {order.user.phone_number}\n"

        text += f"🛒 Состав заказа:\n"
        for item in order.cards:
            name = item.get("name", "—")
            price = item.get("price", 0)
            formatted_price = f"{price:,}".replace(",", " ")
            text += f"• {name} — {formatted_price} сум\n"

        await message.answer(text)
