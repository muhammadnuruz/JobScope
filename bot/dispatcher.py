from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    BOT_TOKEN = os.getenv("TOKEN")
    URL = os.getenv("URL")
    LOGIN = os.getenv("LOGIN")
    PASSWORD = os.getenv("PASSWORD")


bot = Bot(Config.BOT_TOKEN)
dp = Dispatcher(bot=bot, storage=MemoryStorage())
