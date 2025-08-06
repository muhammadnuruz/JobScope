from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.buttons.text import make_application, become_favourite, delete_card, forward_card, plus_1, plus_10, plus_5, \
    close_order, clear_basket, forward_to_bot


async def make_application_button(_id: int):
    design = [
        [InlineKeyboardButton(text=make_application, callback_data=f'make_application_{_id}'),
         InlineKeyboardButton(text=become_favourite, callback_data=f'become_favourite_{_id}')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=design)


def complete_task_button(task_id: int):
    markup = InlineKeyboardMarkup()
    button = InlineKeyboardButton(
        text="✅ Выполнено",
        callback_data=f"complete_task_{task_id}"
    )
    markup.add(button)
    return markup


async def show_application_button(data: dict, user_id: int, phone_number: str, location_link: str, amount: str):
    markup = InlineKeyboardMarkup()
    button = InlineKeyboardButton(
        text="🫣 Посмотреть полный заказ",
        callback_data=f"see_{data['company']}_{user_id}_{phone_number}_{location_link}_{amount}"
    )
    markup.add(button)
    return markup


def display_cards_button(id_: int):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text=delete_card, callback_data=f"delete_card_{id_}"))
    markup.add(InlineKeyboardButton(text=forward_card, callback_data=f"forward_card_{id_}"))
    return markup


def buy_cards_button(id_: int):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text=plus_1, callback_data=f"plus_1_{id_}"),
               InlineKeyboardButton(text=plus_5, callback_data=f"plus_5_{id_}"),
               InlineKeyboardButton(text=plus_10, callback_data=f"plus_10_{id_}"))
    markup.add(InlineKeyboardButton(text=clear_basket, callback_data=f"clear_basket_{id_}"),
               InlineKeyboardButton(text=close_order, callback_data=f"close_order_{id_}"))
    markup.add(InlineKeyboardButton(text=forward_to_bot, url="t.me/TujjorsBot"))
    return markup
