import html
from datetime import datetime

from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import types
import requests

from bot.buttons.text import display_debts
from bot.dispatcher import dp

DEBT_LIST_API = "http://127.0.0.1:8005/api/debts/"
DEBT_DELETE_API = "http://127.0.0.1:8005/api/debts/delete/"


@dp.message_handler(Text(equals=display_debts))
async def show_user_debts(msg: types.Message):
    response = requests.get(DEBT_LIST_API, params={"chat_id": msg.from_user.id})

    if response.status_code != 200:
        await msg.answer("❌ Долги не найдены.")
        return

    debts = response.json()
    results = debts.get('results', [])
    if debts.get('count', 0) == 0 or not results:
        await msg.answer("📭 У вас нет долгов.")
        return

    total_sum = sum(debt.get("amount", 0) for debt in results)
    formatted_total_sum = f"{total_sum:,}".replace(",", " ")
    formatted_total_price = f"{sum(int(d.get('price', 0)) for d in results):,}".replace(",", " ")

    debt_lines = []
    for debt in results:
        borrower_name = html.escape(debt['borrower_name'])
        formatted_amount = f"{int(debt.get('amount', 0)):,}".replace(",", " ")
        debt_lines.append(f"👤 {borrower_name} — {formatted_amount} сум")

    debt_text = "\n".join(debt_lines)

    intro_text = (
        f"📄 Всего долгов: <b>{len(results)}</b>\n"
        f"💰 Общая сумма: <b>{formatted_total_sum} сум</b>\n"
        f"📈 Ежедневный платеж: <b>{formatted_total_price} сум</b>\n"
        f"<b>Список должников:</b>\n"
        f"{debt_text}"
    )
    await msg.answer(intro_text, parse_mode="HTML")

    for debt in results:
        try:
            deadline_date = datetime.strptime(debt['deadline'], "%Y-%m-%d")
            formatted_deadline = deadline_date.strftime("%d-%m-%Y")
        except Exception:
            formatted_deadline = debt['deadline']

        borrower_name = html.escape(debt['borrower_name'])

        formatted_amount = f"{int(debt['amount']):,}".replace(",", " ")
        formatted_price = f"{int(debt['price']):,}".replace(",", " ")

        text = (
            f"👤 <b>{borrower_name}</b> — <b>{formatted_amount} сум</b>\n"
            f"📅 Дата возврата: <b>{formatted_deadline}</b>\n"
            f"📈 Ежедневный платеж: <b>{formatted_price} сум</b>"
        )

        keyboard = InlineKeyboardMarkup().add(
            InlineKeyboardButton("🗑 Удалить", callback_data=f"delete_debt_{debt['id']}")
        )

        await msg.answer(text, reply_markup=keyboard, parse_mode="HTML")


@dp.callback_query_handler(lambda c: c.data.startswith("delete_debt_"))
async def delete_debt_handler(callback_query: types.CallbackQuery):
    debt_id = callback_query.data.split("_")[-1]
    response = requests.delete(f"{DEBT_DELETE_API}{debt_id}/")
    if response.status_code == 204:
        await callback_query.message.edit_text("✅ Долг удалён.")
    else:
        await callback_query.answer("❌ Не удалось удалить долг.")
