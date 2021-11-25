from aiogram import Dispatcher
from aiogram import executor

from loader import db_connector, dispatcher, scheduler
import filters, handlers
from utils.bot_commands import set_bot_commands
from utils.notify_admins import on_startup_notify
from utils.bot_scheduler_tasks import get_all_offices


async def on_startup(dp: Dispatcher):
    await set_bot_commands(dp)
    await on_startup_notify(dp)
    await db_connector.create_users_table()
    await db_connector.create_offices_table()
    await get_all_offices()
    scheduler.add_job(get_all_offices, trigger="cron", hour=1, minute=0)


if __name__ == "__main__":
    scheduler.start()
    executor.start_polling(dispatcher, on_startup=on_startup)
