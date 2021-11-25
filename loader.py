import locale

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from data import creds
from data.types import Emoji
from utils.db_connector import DBConnector
from utils.iis_connector import IisConnector

locale.setlocale(locale.LC_ALL, "ru_RU.UTF-8")
bot = Bot(token=creds.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
bot_id = int(creds.BOT_ID)
dispatcher = Dispatcher(bot=bot, storage=MemoryStorage())
scheduler = AsyncIOScheduler()
db_connector = DBConnector()
iis_connector = IisConnector()
emojis = Emoji()
