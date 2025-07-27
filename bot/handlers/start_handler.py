from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart, Text
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import requests

from bot.buttons.reply_buttons import main_menu_buttons
from bot.buttons.text import skip_txt, back_main_menu, change_location
from bot.dispatcher import dp, bot
from bot.functions.get_advert_function import AIProductManager
from bot.states import RegisterState


@dp.message_handler(Text(equals=[back_main_menu]), state='*')
async def back_main_menu_function_1(msg: types.Message, state: FSMContext):
    await state.finish()
    await msg.answer(text=msg.text, reply_markup=await main_menu_buttons(msg.from_user.id))


@dp.callback_query_handler(Text(equals=[back_main_menu]), state='*')
async def back_main_menu_function_1(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()
    await call.message.answer(text=call.data, reply_markup=await main_menu_buttons(call.from_user.id))


@dp.message_handler(CommandStart())
async def start_register(msg: types.Message, state: FSMContext):
    response = requests.get(f"http://127.0.0.1:8005/api/telegram-users/chat_id/{msg.from_user.id}/")
    if response.status_code != 404:
        await msg.answer(text=f"Бот обновлен ♻", reply_markup=await main_menu_buttons(msg.from_user.id))
    else:
        await state.finish()
        await msg.answer(
            "📱 Пожалуйста, отправьте свой номер телефона:",
            reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(
                KeyboardButton("📱 Отправить номер телефона", request_contact=True)
            )
        )
        await RegisterState.phone_number.set()


@dp.message_handler(content_types=types.ContentType.CONTACT, state=RegisterState.phone_number)
async def get_phone(msg: types.Message, state: FSMContext):
    await state.update_data(phone_number=msg.contact.phone_number)
    await msg.answer(
        "📍 Отправьте свое местоположение:",
        reply_markup=ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
            KeyboardButton("📍 Отправить местоположение", request_location=True)
        )
    )
    await RegisterState.location.set()


@dp.message_handler(content_types=types.ContentType.LOCATION, state=RegisterState.location)
async def get_location(msg: types.Message, state: FSMContext):
    await state.update_data(location_lat=msg.location.latitude, location_lng=msg.location.longitude)
    await msg.answer(
        "📸 Необязательно: отправьте фото или ⏭ Пропустить",
        reply_markup=ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
            KeyboardButton(skip_txt)
        )
    )
    await RegisterState.photo.set()


@dp.message_handler(content_types=types.ContentType.PHOTO, state=RegisterState.photo)
async def get_photo(msg: types.Message, state: FSMContext):
    photo = msg.photo[-1]
    file = await bot.get_file(photo.file_id)
    file_path = file.file_path
    file_bytes = await bot.download_file(file_path)
    await state.update_data(photo_bytes=file_bytes, file_name=f"{msg.from_user.id}.jpg")
    await complete_register(msg, state)


@dp.message_handler(text=skip_txt, state=RegisterState.photo)
async def skip_photo(msg: types.Message, state: FSMContext):
    await state.update_data(photo=None)
    await complete_register(msg, state)


async def complete_register(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    files = {}
    if data.get("photo_bytes"):
        files["photo"] = (data.get("file_name"), data["photo_bytes"].getvalue())
    payload = {
        "chat_id": msg.from_user.id,
        "username": msg.from_user.username,
        "full_name": msg.from_user.full_name,
        "phone_number": data.get("phone_number"),
        "location_lat": data.get("location_lat"),
        "location_lng": data.get("location_lng"),
    }
    response = requests.get(f"http://127.0.0.1:8005/api/telegram-users/chat_id/{msg.from_user.id}/")
    if response.status_code == 404:
        requests.post("http://127.0.0.1:8005/api/telegram-users/create/", data=payload, files=files)
    else:
        tg_user = response.json()
        requests.put(f"http://127.0.0.1:8005/api/telegram-users/update/{tg_user['id']}/", data=payload,
                     files=files)
    await msg.answer("✅ Вы успешно зарегистрировались!", reply_markup=await main_menu_buttons(msg.from_user.id))
    await state.finish()


API_UPDATE_URL = "http://127.0.0.1:8005/api/telegram-users/update/"


@dp.message_handler(text=change_location)
async def start_location_change(msg: types.Message):
    await msg.answer(
        "📍 Пожалуйста, отправьте новую локацию:",
        reply_markup=ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
            KeyboardButton("📍 Отправить местоположение", request_location=True)
        )
    )


@dp.message_handler(content_types=types.ContentType.LOCATION)
async def update_location(msg: types.Message):
    user_id = requests.get(f"http://127.0.0.1:8005/api/telegram-users/chat_id/{msg.from_user.id}/").json()["id"]
    update_payload = {
        "location_lat": msg.location.latitude,
        "location_lng": msg.location.longitude,
    }
    update_response = requests.patch(f"{API_UPDATE_URL}{user_id}/", data=update_payload)
    if update_response.status_code in [200, 202]:
        await msg.answer("✅ Ваша локация успешно обновлена!", reply_markup=await main_menu_buttons(msg.from_user.id))
    else:
        await msg.answer("❗ Произошла ошибка при обновлении локации.")


@dp.message_handler(commands='restart')
async def restart(msg: types.Message):
    manager = AIProductManager()
    await manager.login()
    await manager.embedding_function()
    await msg.answer("Baza yangilandi!")
