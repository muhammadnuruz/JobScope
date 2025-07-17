import logging
import requests
from datetime import datetime

from aiogram import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

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

        users = users_resp.json()

        for user in users['results']:
            chat_id = user["chat_id"]

            debts_resp = requests.get(DEBT_LIST_API, params={"chat_id": chat_id})
            if debts_resp.status_code != 200:
                continue

            debts = debts_resp.json().get("results", [])
            if not debts:
                try:
                    await bot.send_message(chat_id, "📭 У вас нет долгов.")
                except:
                    pass
                continue

            active_debts = []
            for debt in debts:
                deadline = debt.get("deadline")
                try:
                    deadline_date = datetime.strptime(deadline, "%Y-%m-%d").date()
                    if deadline_date >= datetime.today().date():
                        active_debts.append(debt)
                except:
                    pass

            if not active_debts:
                try:
                    await bot.send_message(chat_id, "📭 У вас нет долгов.")
                except:
                    pass
                continue

            total_sum = sum(d.get("price", 0) for d in active_debts)
            formatted_total = f"{total_sum:,.2f}".replace(",", " ").replace(".", ",")

            intro_text = (
                f"📄 Всего долгов: <b>{len(active_debts)}</b>\n"
                f"💰 Общая сумма: <b>{formatted_total} сум</b>\n\n"
                f"<b>Список должников:</b>"
            )
            try:
                await bot.send_message(chat_id, intro_text, parse_mode="HTML")
            except:
                pass

            for debt in active_debts:
                deadline_str = debt.get("deadline", "—")
                try:
                    deadline_date = datetime.strptime(deadline_str, "%Y-%m-%d")
                    formatted_deadline = deadline_date.strftime("%d-%m-%Y")
                except:
                    formatted_deadline = deadline_str

                amount = f"{debt.get('price', 0):,.2f}".replace(",", " ").replace(".", ",")
                price = debt.get("price", "❓")
                if isinstance(price, (int, float)):
                    formatted_price = f"{price:,.2f}".replace(",", " ").replace(".", ",")
                else:
                    formatted_price = price

                text = (
                    f"👤 <b>{debt['borrower_name']}</b> — <b>{amount} сум</b>\n"
                    f"📅 Дата возврата: <b>{formatted_deadline}</b>\n"
                    f"📈 Ежедневный платеж: <b>{formatted_price} сум</b>"
                )

                keyboard = InlineKeyboardMarkup().add(
                    InlineKeyboardButton("🗑 Удалить", callback_data=f"delete_debt_{debt['id']}")
                )
                try:
                    await bot.send_message(chat_id, text, reply_markup=keyboard, parse_mode="HTML")
                except:
                    pass
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
        trigger=CronTrigger(hour=8, minute=0),
    )
    scheduler.add_job(
        delete_expired_debts,
        trigger=CronTrigger(hour=0, minute=0),
    )
    scheduler.start()
    print("✅ Scheduler ishga tushdi.")


admins = [1974800905, 999090234]

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
