from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineQueryResultArticle, InputTextMessageContent, CallbackQuery
from uuid import uuid4
import requests

from bot.buttons.inline_buttons import make_application_button
from bot.buttons.text import search_companies, all_companies
from bot.dispatcher import dp, bot
from bot.states import SearchCompanyState
from bot.buttons.reply_buttons import main_menu_buttons, back_main_menu_button, amount_button

API_URL = "http://127.0.0.1:8005/api/companies/companies/"
FAVOURITES_API_URL = "http://127.0.0.1:8005/api/telegram-users/favourites/"
APPLICATION_URL = "http://127.0.0.1:8005/api/applications/applications/create/"
USER_URL = "http://127.0.0.1:8005/api/telegram-users/chat_id/"


@dp.inline_handler()
async def inline_company_search(inline_query: types.InlineQuery):
    query = inline_query.query.strip()
    params = {'search': query} if query else {}
    response = requests.get(API_URL, params=params)
    results = []

    if response.status_code == 200:
        data = response.json()
        for company in data.get("results", [])[:30]:
            results.append(
                InlineQueryResultArticle(
                    id=str(uuid4()),
                    title=company['name'],
                    description=company.get('description', '—'),
                    input_message_content=InputTextMessageContent(
                        message_text=f"🏢 {company['name']}\n📝 {company.get('description', '—')}\n\nДля заказа: {company['link']}"
                    )
                )
            )
    await inline_query.answer(results, cache_time=1)


@dp.message_handler(regexp=r"^🏢 (.+)")
async def send_company_info(msg: types.Message):
    await msg.delete()
    company_name = msg.text.split("🏢 ")[-1].split("\n")[0]
    response = requests.get(API_URL, params={'search': company_name})
    if response.status_code == 200 and response.json().get("results"):
        company = response.json()['results'][0]
        await msg.answer(
            parse_mode="HTML",
            text=f"🏢 {company['name']}\n📝 {company.get('description', '—')}\n\n<a href='{company['link']}'>Для заказа</a>",
            reply_markup=await make_application_button(company['id'])
        )


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
    query = msg.text.strip()
    response = requests.get(API_URL, params={'search': query}) if query else requests.get(API_URL)

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
    response = requests.post(APPLICATION_URL, data=payload)
    if response.status_code in [200, 201]:
        await msg.answer("✅ Ваша заявка успешно отправлена!", reply_markup=await main_menu_buttons(msg.from_user.id))
    else:
        await msg.answer("❗ Произошла ошибка при отправке заявки.")

    res_company = requests.get(f"{API_URL}{data['company_id']}/").json()
    user = requests.get(f"{USER_URL}{msg.from_user.id}/").json()
    location_link = f"https://maps.google.com/?q={user['location_lat']},{user['location_lng']}"
    try:
        await bot.send_message(
            chat_id=res_company['group_id'],
            text=(
                f"📥 Новое приложение!\n"
                f"👤 Пользователь: <a href='tg://user?id={msg.from_user.id}'>{msg.from_user.full_name}</a>\n"
                f"📲 Номер телефона: {user['phone_number']}\n"
                f"🏢 Компания: {res_company['name']}\n"
                f"💰 Предлагаемая сумма: {amount}\n"
                f"📍 <a href='{location_link}'>Расположение</a>"
            ),
            parse_mode="HTML"
        )
    except Exception:
        pass
    await state.finish()


@dp.callback_query_handler(lambda c: c.data.startswith("become_favourite_"))
async def become_favourite_handler(call: types.CallbackQuery, state: FSMContext):
    company_id = int(call.data.split("_")[-1])
    telegram_user = requests.get(f"{USER_URL}{call.from_user.id}").json()
    payload = {
        "user": telegram_user['id'],
        "company": company_id
    }
    requests.post(FAVOURITES_API_URL, data=payload)
    await call.answer("⭐ Компания добавлена ​​в избранное!", show_alert=True)
