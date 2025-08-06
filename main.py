import logging
from aiogram import executor
from bot.dispatcher import dp
from bot.functions.main import on_startup
from bot import handlers

admins = [1974800905, 999090234]

# Loggerlar darajasini warning yoki yuqoriga tushirish
logging.basicConfig(level=logging.WARNING)
logging.getLogger("aiogram").setLevel(logging.WARNING)
logging.getLogger("aiohttp").setLevel(logging.WARNING)
logging.getLogger("asyncio").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
