from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from bot.buttons.text import back_main_menu, adverts, none_advert, forward_advert, change_location, favourite_companies, \
    search_companies, near_shops, active_tasks, all_active_tasks, create_task, all_companies
import requests


async def main_menu_buttons(chat_id: int):
    response = requests.get(f"http://127.0.0.1:8005/api/telegram-users/chat_id/{chat_id}/")
    user = response.json()
    if user.get("status") == "customer":
        buttons = [
            [KeyboardButton(all_companies)],
            [KeyboardButton(search_companies)],
            [KeyboardButton(favourite_companies)],
            [KeyboardButton(change_location)]
        ]

    elif user.get("status") == "manager":
        buttons = [
            [KeyboardButton(create_task)],
            [KeyboardButton(all_active_tasks)],
            [KeyboardButton(near_shops)]
        ]
    else:
        buttons = [
            [KeyboardButton(active_tasks)],
            [KeyboardButton(near_shops)]
        ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)


async def back_main_menu_button():
    design = [[back_main_menu]]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)


async def admin_menu_buttons():
    design = [
        [adverts],
        [back_main_menu]
    ]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)


async def advert_menu_buttons():
    design = [
        [none_advert, forward_advert],
        [back_main_menu]
    ]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)


async def amount_button():
    design = [
        ['1', '2'],
        ['4', '3'],
        ['5', '6'],
        ['8', '7'],
        ['9', '10'],
        [back_main_menu],
    ]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)
