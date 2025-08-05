from aiogram.dispatcher.filters import Text
from aiogram import types

from bot.buttons.inline_buttons import display_cards_button, buy_cards_button
from bot.buttons.reply_buttons import request_chat_reply_keyboard, main_menu_buttons
from bot.buttons.text import display_cards
from bot.config import get_all_cards, get_card_by_id, delete_card_by_id
from bot.dispatcher import dp


@dp.message_handler(Text(equals=display_cards))
async def show_my_cards_1(msg: types.Message):
    cards = await get_all_cards(msg.from_user.id)
    if not cards:
        await msg.answer(text="💳 У вас нет карты.")
    else:
        for card in cards:
            caption = f"📎 {card.name}\n💰 {card.price} so'm"
            await msg.answer_photo(
                photo=card.imageUrl,
                caption=caption,
                reply_markup=display_cards_button(id_=card.id)
            )


@dp.callback_query_handler(lambda c: c.data.startswith("forward_card_"))
async def ask_where_to_forward(call: types.CallbackQuery):
    card_id = int(call.data.split('_')[-1])
    card = await get_card_by_id(card_id)

    if not card:
        await call.answer("⛔ Карточка не найдена.", show_alert=True)
        return
    await call.message.delete()
    await call.message.answer(
        "📤 Куда отправить эту карточку?",
        reply_markup=request_chat_reply_keyboard(card_id)
    )


@dp.message_handler(content_types=['chat_shared'])
async def handle_chat_selection(msg: types.Message):
    chat_shared = msg.chat_shared

    request_id = chat_shared['request_id']
    chat_id = chat_shared['chat_id']

    try:
        card = await get_card_by_id(request_id)
        if card:
            caption = f"📎 {card.name}\n💰 {card.price} сум"
            await msg.bot.send_photo(
                chat_id=chat_id,
                photo=card.imageUrl,
                caption=caption,
                reply_markup=buy_cards_button(id_=card.id)
            )
            await msg.answer("Сообщение было отправлено на ваш канал/группу. ✅",
                             reply_markup=await main_menu_buttons(msg.from_user.id))
    except Exception as e:
        await msg.answer(f"❌ Для начала сделайте бота администратором вашего канала/группы.",
                         reply_markup=await main_menu_buttons(msg.from_user.id))


@dp.callback_query_handler(lambda c: c.data.startswith("delete_card_"))
async def handle_delete_card(call: types.CallbackQuery):
    id_ = int(call.data.split("_")[-1])
    deleted = await delete_card_by_id(id_)
    if deleted:
        await call.message.edit_caption("❌ Карта удалена.")
    else:
        await call.answer("⛔ Карта не найдена.", show_alert=True)
