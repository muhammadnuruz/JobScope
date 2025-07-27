from aiogram import Dispatcher
from pytz import timezone
import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from bot.functions.delete_debts import delete_expired_debts
from bot.functions.get_advert_function import AIProductManager
from bot.functions.send_daily_debts import daily_check
import logging

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()


async def run_get_advert():
    manager = AIProductManager()
    await manager.get_advert()


async def on_startup(dp: Dispatcher):
    scheduler.add_job(
        daily_check,
        trigger=CronTrigger(hour=8, minute=0, timezone=timezone("Asia/Tashkent")),
    )
    scheduler.add_job(
        func=lambda: asyncio.create_task(run_get_advert()),
        trigger=CronTrigger(hour=8, minute=0, timezone=timezone("Asia/Tashkent")),
    )
    scheduler.add_job(
        delete_expired_debts,
        trigger=CronTrigger(hour=0, minute=0, timezone=timezone("Asia/Tashkent")),
    )
    scheduler.start()
    logger.info("✅ Scheduler ishga tushdi.")
