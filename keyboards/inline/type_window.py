from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import type_window_callback
from loader import emojis

typewindowmenu = InlineKeyboardMarkup(row_width=1)
typewindowmenu.insert(InlineKeyboardButton(text=f"{emojis.technologist} Оператор",
                                           callback_data=type_window_callback.new(
                                               action="window_choice", type_window=1)))
typewindowmenu.insert(InlineKeyboardButton(text=f"{emojis.judge} Юрист",
                                           callback_data=type_window_callback.new(
                                               action="window_choice", type_window=2)))
typewindowmenu.insert(InlineKeyboardButton(text=f"{emojis.card_index_dividers} Выдача готового результата",
                                           callback_data=type_window_callback.new(
                                               action="window_choice", type_window=3)))
typewindowmenu.insert(InlineKeyboardButton(text=f"{emojis.right_arrow_curving_left} Вернуться к выбору времени",
                                           callback_data=type_window_callback.new(
                                               action="step_back", type_window=0)))
typewindowmenu.insert(InlineKeyboardButton(text=f"{emojis.home} Главное меню",
                                           callback_data=type_window_callback.new(
                                               action="backtotop", type_window=0)))
