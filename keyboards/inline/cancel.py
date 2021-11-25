from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import cancel_callback
from loader import emojis

cancelmenu = InlineKeyboardMarkup(row_width=1)
cancelmenu.insert(InlineKeyboardButton(text=f"{emojis.cross_mark} Отмена",
                                       callback_data=cancel_callback.new(action="cancel")))
