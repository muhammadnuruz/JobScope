from aiogram import types
import requests

from bot.buttons.inline_buttons import make_application_button
from bot.buttons.text import favourite_companies
from bot.dispatcher import dp


@dp.message_handler(text=favourite_companies)
async def show_favourite_companies(msg: types.Message):
    favourite_ids = requests.get(f"http://127.0.0.1:8005/api/telegram-users/chat_id/{msg.from_user.id}/").json().get(
        "favourite_companies", [])
    if not favourite_ids:
        await msg.answer("⚠️ У вас нет избранных компаний.")
        return
    await msg.answer("⭐ Ваши избранные компании:")
    for company_id in favourite_ids:
        company_res = requests.get(f"http://127.0.0.1:8005/api/companies/companies/{company_id}/")
        if company_res.status_code == 200:
            company = company_res.json()
            await msg.answer(
                text=f"🏢 {company['name']}\n📝 {company.get('description', '—')}",
                reply_markup=await make_application_button(company['id'])
            )
        else:
            continue
