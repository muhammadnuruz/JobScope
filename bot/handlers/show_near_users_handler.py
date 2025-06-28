import os

from aiogram import types
import requests
from aiogram.dispatcher import FSMContext
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from bot.buttons.reply_buttons import main_menu_buttons
from bot.buttons.text import near_shops, back_main_menu
from bot.dispatcher import dp
from bot.states import NearbyUserState

NEARBY_USERS_API = "http://127.0.0.1:8005/api/telegram-users/nearby-users/"


@dp.message_handler(text=near_shops)
async def request_live_location(msg: types.Message, state: FSMContext):
    await msg.answer(
        "📍 Пожалуйста, отправьте вашу текущую локацию:",
        reply_markup=ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
            KeyboardButton("📍 Отправить локацию", request_location=True)
        ).add(KeyboardButton(text=back_main_menu)),
    )
    await state.set_state(NearbyUserState.waiting_for_location)


MEDIA_ROOT = "/home/muhammadnur/PycharmProjects/telegram-bots/JobScope"


@dp.message_handler(content_types=types.ContentType.LOCATION, state=NearbyUserState.waiting_for_location)
async def handle_live_location(msg: types.Message, state: FSMContext):
    lat = msg.location.latitude
    lng = msg.location.longitude
    response = requests.get(
        "http://127.0.0.1:8005/api/telegram-users/nearby-users/",
        params={"lat": lat, "lng": lng}
    )
    if response.status_code != 200:
        await msg.answer("❗ Не удалось получить пользователей поблизости.")
        await state.finish()
        return
    nearby_users = response.json()
    if not nearby_users:
        await msg.answer("🤷 Поблизости пользователей не найдено.")
        await state.finish()
        return
    for user in nearby_users:
        name = user.get("full_name") or user.get("username") or str(user.get("chat_id"))
        phone = user.get("phone_number", "—")
        user_lat = user.get("location_lat")
        user_lng = user.get("location_lng")
        photo_path = user.get("photo")
        location_link = f"https://maps.google.com/?q={user_lat},{user_lng}"
        text = f"""
👤 <b>{name}</b>
📞 <code>{phone}</code>
📍 <a href="{location_link}">Расположение</a>
"""
        if photo_path:
            full_path = MEDIA_ROOT + photo_path
            if os.path.exists(full_path):
                with open(full_path, "rb") as photo_file:
                    await msg.answer_photo(photo=photo_file, caption=text, parse_mode="HTML")
            else:
                await msg.answer(f"{text}\n⚠️ Файл не найден.", parse_mode="HTML")
        else:
            await msg.answer(text, parse_mode="HTML")
    await msg.answer("🔙 Главное меню", reply_markup=await main_menu_buttons(msg.from_user.id))
    await state.finish()
