from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import unsubscribe_callback
from loader import emojis

unsubscribemenu = InlineKeyboardMarkup(row_width=1)
unsubscribemenu.insert(InlineKeyboardButton(text=f"{emojis.cross_mark} Удалить свои персональные данные",
                                            callback_data=unsubscribe_callback.new(action="cancel")))
unsubscribemenu.insert(InlineKeyboardButton(text=f"{emojis.home} Главное меню",
                                            callback_data=unsubscribe_callback.new(action="backtotop")))
