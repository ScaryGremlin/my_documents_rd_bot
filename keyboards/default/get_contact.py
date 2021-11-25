from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from loader import emojis

get_contact_def_menu = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
get_contact_def_menu.insert(KeyboardButton(text=f"{emojis.mobile_phone} Поделиться номером телефона",
                                           request_contact=True))
get_contact_def_menu.insert(KeyboardButton(text=f"{emojis.home} Главное меню"))
