from aiogram.types import CallbackQuery

from bot.config import get_card_by_id, get_user_by_chat_id, save_basket_to_db, get_baskets
from bot.dispatcher import dp


@dp.callback_query_handler(lambda c: c.data.startswith("plus_"))
async def ordering_function(call: CallbackQuery):
    tg_user = await get_user_by_chat_id(call.from_user.id)
    if tg_user:
        _, num, id_ = call.data.split("_")
        card = await get_card_by_id(id_=id_)
        await save_basket_to_db(shop_id=card.user.id, user_id=tg_user.id, card_id=card.id, count=int(num))
        await call.answer(f"🧺 {num} товаров добавлено в корзину", show_alert=True)
    else:
        await call.answer(f"⛔ Сначала зарегистрируйтесь у бота.\n\n👉 t.me/TujjorSBot", show_alert=True)


@dp.callback_query_handler(lambda c: c.data.startswith("close_order_"))
async def ordering_function_2(call: CallbackQuery):
    tg_user = await get_user_by_chat_id(call.from_user.id)
    if tg_user:
        id_ = call.data.split("_")[-1]
        card = await get_card_by_id(id_=id_)
        baskets = await get_baskets(shop_id=card.user.id, user_id=tg_user.id)
    else:
        await call.answer(f"⛔ Сначала зарегистрируйтесь у бота.\n\n👉 t.me/TujjorSBot", show_alert=True)
