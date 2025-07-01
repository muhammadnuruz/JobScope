from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
import requests

from bot.buttons.inline_buttons import make_application_button
from bot.buttons.text import search_companies, all_companies
from bot.dispatcher import dp, bot
from bot.states import SearchCompanyState
from bot.buttons.reply_buttons import main_menu_buttons, back_main_menu_button, amount_button

API_URL = "http://127.0.0.1:8005/api/companies/companies/"


@dp.message_handler(text=all_companies)
async def get_all_companies(msg: types.Message):
    response = requests.get(API_URL)
    if response.status_code == 200:
        companies = response.json()
        if not companies.get("results"):
            await msg.answer("❌ Компания не найдена.")
        else:
            await msg.answer(text="🔍 Найденные компании:")
            for company in companies['results']:
                await msg.answer(
                    parse_mode="HTML",
                    text=f"🏢 {company['name']}\n📝 {company.get('description', '—')}\n\n<a href='{company['link']}'>Для заказа</a>",
                    reply_markup=await make_application_button(company['id'])
                )
    else:
        await msg.answer("❗ Произошла ошибка при поиске..")


@dp.message_handler(text=search_companies)
async def start_company_search(msg: types.Message):
    await msg.answer("🔎 Введите название компании для поиска:", reply_markup=await back_main_menu_button())
    await SearchCompanyState.waiting_for_query.set()


@dp.message_handler(state=SearchCompanyState.waiting_for_query)
async def perform_search(msg: types.Message, state: FSMContext):
    query = msg.text
    response = requests.get(API_URL, params={'search': query})

    if response.status_code == 200:
        companies = response.json()
        if not companies.get("results"):
            await msg.answer("❌ Компания с таким названием не найдена.")
        else:
            await msg.answer(text="🔍 Найденные компании:")
            for company in companies['results']:
                await msg.answer(
                    parse_mode="HTML",
                    text=f"🏢 {company['name']}\n📝 {company.get('description', '—')}\n\n<a href='{company['link']}'>Для заказа</a>",
                    reply_markup=await make_application_button(company['id'])
                )
    else:
        await msg.answer("❗ Произошла ошибка при поиске..")

    await state.finish()


@dp.callback_query_handler(lambda c: c.data.startswith("make_application_"))
async def start_application(call: CallbackQuery, state: FSMContext):
    company_id = int(call.data.split("_")[-1])
    await state.update_data(company_id=company_id)
    await call.message.answer("💰 Выберите желаемую сумму (1 = 100 000 сум):", reply_markup=await amount_button())
    await SearchCompanyState.waiting_for_amount.set()
    await call.answer()


@dp.message_handler(state=SearchCompanyState.waiting_for_amount)
async def submit_application(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    amount = msg.text + "00000"
    payload = {
        "chat_id": msg.from_user.id,
        "company": data['company_id'],
        "amount_requested": amount
    }
    response = requests.post("http://127.0.0.1:8005/api/applications/applications/create/", data=payload)
    if response.status_code in [200, 201]:
        await msg.answer("✅ Ваша заявка успешно отправлена!", reply_markup=await main_menu_buttons(msg.from_user.id))
    else:
        await msg.answer("❗ Произошла ошибка при отправке заявки.")
    res_company = requests.get(f"http://127.0.0.1:8005/api/companies/companies/{data['company_id']}/").json()
    response = requests.get(f"http://127.0.0.1:8005/api/telegram-users/chat_id/{msg.from_user.id}/")
    user = response.json()
    location_link = f"https://maps.google.com/?q={user['location_lat']},{user['location_lng']}"
    try:
        await bot.send_message(
            chat_id=res_company['group_id'],
            text=(
                f"📥 Новое приложение!\n"
                f"👤 Пользователь: <a href='tg://user?id={msg.from_user.id}'>{msg.from_user.full_name}</a>\n"
                f"🏢 Компания: {res_company['name']}\n"
                f"💰 Предлагаемая сумма: {amount}\n"
                f"📍 <a href='{location_link}'>Расположение</a>"
            ),
            parse_mode="HTML"
        )
    except Exception:
        pass
    await state.finish()


FAVOURITES_API_URL = "http://127.0.0.1:8005/api/telegram-users/favourites/"


@dp.callback_query_handler(lambda c: c.data.startswith("become_favourite_"))
async def become_favourite_handler(call: types.CallbackQuery, state: FSMContext):
    company_id = int(call.data.split("_")[-1])
    telegram_user = requests.get(f"http://127.0.0.1:8005/api/telegram-users/chat_id/{call.from_user.id}").json()
    payload = {
        "user": telegram_user['id'],
        "company": company_id
    }
    requests.post(FAVOURITES_API_URL, data=payload)
    await call.answer("⭐ Компания добавлена ​​в избранное!", show_alert=True)
