import logging
from aiogram import executor
from bot.dispatcher import dp
from bot.functions.main import on_startup
from bot import handlers

admins = [1974800905, 999090234]

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
