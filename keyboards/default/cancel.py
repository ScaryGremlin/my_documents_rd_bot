from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from loader import emojis

cancel_def_menu = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
cancel_def_menu.insert(KeyboardButton(text=f"{emojis.cross_mark} Отмена"))
