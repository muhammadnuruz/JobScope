import asyncio
from aiogram import Dispatcher
from pytz import timezone

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from bot.functions.delete_debts import delete_expired_debts
from bot.functions.get_advert_function import AIProductManager, get_advert
from bot.functions.send_daily_debts import daily_check

scheduler = AsyncIOScheduler()


def run_get_advert():
    loop = asyncio.get_event_loop()
    loop.create_task(get_advert())


async def on_startup(dp: Dispatcher):
    manager = AIProductManager()
    await manager.login()

    scheduler.add_job(
        daily_check,
        trigger=CronTrigger(hour=8, minute=0, timezone=timezone("Asia/Tashkent")),
    )
    # scheduler.add_job(
    #     func=run_get_advert,
    #     trigger=CronTrigger(hour=8, minute=0, timezone=timezone("Asia/Tashkent")),
    # )
    scheduler.add_job(
        delete_expired_debts,
        trigger=CronTrigger(hour=0, minute=0, timezone=timezone("Asia/Tashkent")),
    )
    scheduler.start()
    print("✅ Scheduler ishga tushdi.")
