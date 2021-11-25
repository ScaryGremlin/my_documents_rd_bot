from aiogram import types
from aiogram.dispatcher.filters import CommandStart

from keyboards.inline.main import mainmenu
from loader import dispatcher


@dispatcher.message_handler(CommandStart())
async def main_menu(message: types.Message):
    await message.answer("Добро пожаловать в главное меню, вот что здесь есть:",
                         reply_markup=mainmenu)
