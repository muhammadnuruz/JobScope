from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
import requests

from bot.buttons.reply_buttons import main_menu_buttons, back_main_menu_button
from bot.buttons.text import create_debt
from bot.dispatcher import dp
from aiogram.dispatcher.filters import Text

DEBT_CREATE_API = "http://127.0.0.1:8005/api/debts/create/"


@dp.message_handler(Text(equals=create_debt))
async def start_debt_creation(msg: types.Message, state: FSMContext):
    await msg.answer("👤 Введите имя:", reply_markup=await back_main_menu_button())
    await state.set_state("debt_borrower_name")


@dp.message_handler(state="debt_borrower_name")
async def get_borrower_name(msg: types.Message, state: FSMContext):
    await state.update_data(borrower_name=msg.text)
    await msg.answer("💰 Введите сумму долга (например: 150000):")
    await state.set_state("debt_amount")


@dp.message_handler(state="debt_amount")
async def get_amount(msg: types.Message, state: FSMContext):
    try:
        amount = int(msg.text)
        await state.update_data(amount=amount)
    except ValueError:
        await msg.answer("⚠️ Введите корректную сумму.")
        return
    await msg.answer("📅 Введите дату возврата (например: 01-08-2025):")
    await state.set_state("debt_deadline")


import locale

locale.setlocale(locale.LC_ALL, '')


@dp.message_handler(state="debt_deadline")
async def get_deadline(msg: types.Message, state: FSMContext):
    await state.update_data(deadline=msg.text)
    data = await state.get_data()

    try:
        deadline_date = datetime.strptime(data["deadline"], "%d-%m-%Y").date()
        today = datetime.today().date()
        remaining_days = (deadline_date - today).days

        if remaining_days <= 0:
            await msg.answer("⚠️ Дата не должна быть в прошлом или совпадать с сегодняшним днем.")
            return

        price_per_day = int(data["amount"] / remaining_days)

        formatted_deadline = deadline_date.strftime("%Y-%m-%d")

    except Exception:
        await msg.answer("❌ Дата введена в неправильном формате. Формат: ДД-ММ-ГГГГ (например: 01-08-2025).")
        return

    payload = {
        "borrower_name": data["borrower_name"],
        "amount": data["amount"],
        "deadline": formatted_deadline,
        "chat_id": msg.from_user.id,
        "price": price_per_day
    }

    response = requests.post(
        DEBT_CREATE_API,
        json=payload,
    )

    if response.status_code in [200, 201]:
        await msg.answer("✅ Долг успешно добавлен!", reply_markup=await main_menu_buttons(msg.from_user.id))
    else:
        await msg.answer("❌ Ошибка при добавлении долга.", reply_markup=await main_menu_buttons(msg.from_user.id))
    await state.finish()
