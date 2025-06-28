import logging
from aiogram import executor
from bot import handlers
from bot.dispatcher import dp

admins = [1974800905]

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)
