from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.buttons.text import make_application, become_favourite


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
