import html
import logging
import requests
from datetime import datetime

from aiogram import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pytz import timezone

from bot import handlers
from bot.dispatcher import dp, bot
from aiogram import Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

DEBT_LIST_API = "http://127.0.0.1:8005/api/debts/"
DEBT_DELETE_API = "http://127.0.0.1:8005/api/debts/delete/"
USER_LIST_API = "http://127.0.0.1:8005/api/telegram-users/"


async def daily_check():
    try:
        users_resp = requests.get(USER_LIST_API)
        if users_resp.status_code != 200:
            print("❌ Foydalanuvchilarni olishda xatolik.")
            return

        users = users_resp.json().get("results", [])

        for user in users:
            chat_id = user["chat_id"]

            debts_resp = requests.get(DEBT_LIST_API, params={"chat_id": chat_id})
            if debts_resp.status_code != 200:
                continue

            all_debts = debts_resp.json().get("results", [])
            active_debts = []

            for debt in all_debts:
                try:
                    deadline = datetime.strptime(debt["deadline"], "%Y-%m-%d").date()
                    if deadline >= datetime.today().date():
                        active_debts.append(debt)
                except:
                    continue

            if not active_debts:
                continue

            total_sum = sum(d["amount"] for d in active_debts)
            total_daily = sum(d.get("price", 0) for d in active_debts)

            formatted_total = f"{total_sum:,}".replace(",", " ")
            formatted_daily = f"{total_daily:,}".replace(",", " ")
            debt_lines = []
            for debt in active_debts:
                borrower_name = html.escape(debt["borrower_name"])
                formatted_amount = f"{debt['amount']:,}".replace(",", " ")
                debt_lines.append(f"👤 {borrower_name} — {formatted_amount} сум")

            debt_text = "\n".join(debt_lines)

            message = (
                f"📄 Всего долгов: <b>{len(active_debts)}</b>\n"
                f"💰 Общая сумма: <b>{formatted_total} сум</b>\n"
                f"📈 Ежедневный платеж: <b>{formatted_daily} сум</b>\n"
                f"<b>Список должников:</b>\n"
                f"{debt_text}"
            )
            try:
                await bot.send_message(chat_id, message, parse_mode="HTML")
            except:
                continue

            for debt in active_debts:
                try:
                    deadline = datetime.strptime(debt["deadline"], "%Y-%m-%d")
                    formatted_deadline = deadline.strftime("%d-%m-%Y")
                except:
                    formatted_deadline = debt["deadline"]

                formatted_amount = f"{debt['amount']:,}".replace(",", " ")
                formatted_price = f"{debt['price']:,}".replace(",", " ")

                borrower_name = html.escape(debt['borrower_name'])

                text = (
                    f"👤 <b>{borrower_name}</b> — <b>{formatted_amount} сум</b>\n"
                    f"📅 Дата возврата: <b>{formatted_deadline}</b>\n"
                    f"📈 Ежедневный платеж: <b>{formatted_price} сум</b>"
                )

                keyboard = InlineKeyboardMarkup().add(
                    InlineKeyboardButton("🗑 Удалить", callback_data=f"delete_debt_{debt['id']}")
                )

                try:
                    await bot.send_message(chat_id, text, reply_markup=keyboard, parse_mode="HTML")
                except:
                    continue
    except Exception as e:
        print("Xatolik:", e)


async def delete_expired_debts():
    try:
        users_resp = requests.get(USER_LIST_API)
        if users_resp.status_code != 200:
            print("❌ Foydalanuvchilarni olishda xatolik.")
            return

        users = users_resp.json()

        for user in users['results']:
            chat_id = user["chat_id"]

            debts_resp = requests.get(DEBT_LIST_API, params={"chat_id": chat_id})
            if debts_resp.status_code != 200:
                continue

            debts = debts_resp.json().get("results", [])
            for debt in debts:
                deadline = debt.get("deadline")
                try:
                    deadline_date = datetime.strptime(deadline, "%Y-%m-%d").date()
                    if deadline_date < datetime.today().date():
                        requests.delete(f"{DEBT_DELETE_API}{debt['id']}/")
                        print(f"🗑 Qarz o'chirildi: {debt['borrower_name']}")
                except Exception as e:
                    print("🛑 Sana xatosi:", e)

    except Exception as e:
        print("Xatolik:", e)


scheduler = AsyncIOScheduler()


async def on_startup(dp: Dispatcher):
    scheduler.add_job(
        daily_check,
        trigger=CronTrigger(hour=8, minute=0, timezone=timezone("Asia/Tashkent")),
    )
    scheduler.add_job(
        delete_expired_debts,
        trigger=CronTrigger(hour=0, minute=0, timezone=timezone("Asia/Tashkent")),
    )
    scheduler.start()
    print("✅ Scheduler ishga tushdi.")


admins = [1974800905, 999090234]

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
