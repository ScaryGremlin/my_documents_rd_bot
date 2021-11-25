from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import main_callback
from loader import emojis

mainmenu = InlineKeyboardMarkup(row_width=1)
mainmenu.insert(InlineKeyboardButton(text=f"{emojis.card_index_dividers} Сообщить ФИО и номер телефона",
                                     callback_data=main_callback.new(action="transmit_personal_data")))
mainmenu.insert(InlineKeyboardButton(text=f"{emojis.clipboard} Проверка дела",
                                     callback_data=main_callback.new(action="case_status")))
mainmenu.insert(InlineKeyboardButton(text=f"{emojis.office_building} Наши отделения",
                                     switch_inline_query_current_chat="offices"))
mainmenu.insert(InlineKeyboardButton(text=f"{emojis.card_file_box} Перечень услуг",
                                     callback_data=main_callback.new(action="service_list")))
mainmenu.insert(InlineKeyboardButton(text=f"{emojis.red_question_mark} Задать вопрос",
                                     callback_data=main_callback.new(action="ask_a_question")))
