from aiogram.dispatcher.filters import Text
from aiogram import types

from bot.buttons.inline_buttons import display_cards_button, buy_cards_button
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
async def show_my_cards_2(call: types.CallbackQuery):
    id_ = call.data.split('_')[-1]
    card = await get_card_by_id(id_)
    if card:
        await call.message.delete()
        caption = f"📎 {card.name}\n💰 {card.price} сум"
        message = await call.message.answer_photo(
            photo=card.imageUrl,
            caption=caption,
            reply_markup=buy_cards_button(id_=card.id)
        )
        await message.reply(
            "ℹ️ Чтобы отправить эту карточку в нужный канал:\n"
            "— нажмите на сообщение с карточкой\n"
            "— затем выберите нужный канал или чат для пересылки.",
            parse_mode="HTML"
        )
    else:
        await call.answer(text="⛔ Такого продукта не существует.", show_alert=True)


@dp.callback_query_handler(lambda c: c.data.startswith("delete_card_"))
async def handle_delete_card(call: types.CallbackQuery):
    id_ = int(call.data.split("_")[-1])
    deleted = await delete_card_by_id(id_)
    if deleted:
        await call.message.edit_caption("❌ Карта удалена.")
    else:
        await call.answer("⛔ Карта не найдена.", show_alert=True)
