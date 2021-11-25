from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import backtotop_callback
from loader import emojis

backtotopmenu = InlineKeyboardMarkup(row_width=1)
backtotopmenu.insert(InlineKeyboardButton(text=f"{emojis.home} Главное меню",
                                          callback_data=backtotop_callback.new(action="backtotop")))
