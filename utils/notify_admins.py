from aiogram import Dispatcher

from data.creds import BOT_ADMINS


async def on_startup_notify(dispatcher: Dispatcher):
    for admin in BOT_ADMINS:
        try:
            await dispatcher.bot.send_message(admin, "Бот запущен и готов к работе!")
            # Записать в лог
        except Exception as error:
            print(error)
