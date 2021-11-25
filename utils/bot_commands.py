from aiogram import Dispatcher
from aiogram.types import BotCommand


async def set_bot_commands(dispatcher: Dispatcher):
    await dispatcher.bot.set_my_commands([
        BotCommand("start", "давайте начнём!"),
    ])
