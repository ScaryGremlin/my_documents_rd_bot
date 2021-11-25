import calendar
from datetime import datetime, timedelta

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from keyboards.inline.callback_datas import calendar_callback, time_calendar_callback
from keyboards.inline.main import mainmenu
from loader import emojis


def create_calendar(year=datetime.now().year, month=datetime.now().month,
                    pre_entry_dates: list = None) -> InlineKeyboardMarkup:
    """

    :param year:
    :param month:
    :param pre_entry_dates:
    :return:
    """
    inline_kb = InlineKeyboardMarkup(row_width=7)
    ignore_callback = calendar_callback.new("ignore", year, month, 0)  # Кнопка без ответа

    # Первая строка - месяц и год
    inline_kb.row()
    inline_kb.insert(InlineKeyboardButton("<<", callback_data=calendar_callback.new("prev_year", year, month, 1)))
    inline_kb.insert(InlineKeyboardButton(f'{calendar.month_name[month]} {str(year)}', callback_data=ignore_callback))
    inline_kb.insert(InlineKeyboardButton(">>", callback_data=calendar_callback.new("next_year", year, month, 1)))

    # Вторая строка - день недели
    inline_kb.row()
    for day in ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]:
        inline_kb.insert(InlineKeyboardButton(day, callback_data=ignore_callback))

    # Строки календаря - дни месяца
    month_calendar = calendar.monthcalendar(year, month)
    for week in month_calendar:
        inline_kb.row()
        for day in week:
            if day == 0:
                inline_kb.insert(InlineKeyboardButton(" ", callback_data=ignore_callback))
            else:
                date = datetime(year, month, day).date()
                if date in pre_entry_dates:
                    inline_kb.insert(InlineKeyboardButton(str(day),
                                                          callback_data=calendar_callback.new("day", year, month, day)))
                else:
                    inline_kb.insert(InlineKeyboardButton(f"{emojis.cross_mark}",
                                                          callback_data=ignore_callback))

    # Предпоследняя строка - перемещение между месяцами
    inline_kb.row()
    inline_kb.insert(InlineKeyboardButton("<", callback_data=calendar_callback.new("prev_month", year, month, day)))
    inline_kb.insert(InlineKeyboardButton(" ", callback_data=ignore_callback))
    inline_kb.insert(InlineKeyboardButton(">", callback_data=calendar_callback.new("next_month", year, month, day)))

    # Последняя строка - возврат в главное меню
    inline_kb.row()
    inline_kb.insert(InlineKeyboardButton(text=f"{emojis.home} Главное меню",
                                          callback_data=calendar_callback.new("main_menu", year, month, 0)))
    return inline_kb


async def process_calendar_selection(query: CallbackQuery, data: dict, pre_entry_dates: list) -> tuple:
    """

    :param query:
    :param data:
    :param pre_entry_dates:
    :return:
    """
    return_data = (False, None)
    temp_date = datetime(int(data["year"]), int(data["month"]), 1).date()
    # processing empty buttons, answering with no action
    if data["act"] == "ignore":
        await query.answer(cache_time=60)
    # user picked a day button, return date
    elif data["act"] == "day":
        await query.message.delete_reply_markup()   # removing inline keyboard
        return_data = True, datetime(int(data["year"]), int(data["month"]), int(data["day"])).date()
    # user navigates to previous year, editing message with new calendar
    elif data["act"] == "prev_year":
        prev_date = temp_date - timedelta(days=365)
        await query.message.edit_reply_markup(create_calendar(int(prev_date.year),
                                                              int(prev_date.month),
                                                              pre_entry_dates))
    # user navigates to next year, editing message with new calendar
    elif data["act"] == "next_year":
        next_date = temp_date + timedelta(days=365)
        await query.message.edit_reply_markup(create_calendar(int(next_date.year),
                                                              int(next_date.month),
                                                              pre_entry_dates))
    # user navigates to previous month, editing message with new calendar
    elif data["act"] == "prev_month":
        prev_date = temp_date - timedelta(days=1)
        await query.message.edit_reply_markup(create_calendar(int(prev_date.year),
                                                              int(prev_date.month),
                                                              pre_entry_dates))
    # user navigates to next month, editing message with new calendar
    elif data["act"] == "next_month":
        next_date = temp_date + timedelta(days=31)
        await query.message.edit_reply_markup(reply_markup=create_calendar(int(next_date.year),
                                                                           int(next_date.month),
                                                                           pre_entry_dates))
    elif data["act"] == "main_menu":
        await query.message.edit_text("Добро пожаловать в главное меню, вот что здесь есть:")
        await query.message.edit_reply_markup(reply_markup=mainmenu)
    else:
        await query.message.answer(f"{emojis.thinking_face} Что-то пошло не так...")
    # at some point user clicks DAY button, returning date
    return return_data


def create_time_kb(pre_entry_times: list) -> InlineKeyboardMarkup:
    """

    :param pre_entry_times:
    :return:
    """
    inline_kb = InlineKeyboardMarkup(row_width=6)
    inline_kb.row()
    for time in pre_entry_times:
        # Поменять в строке символ двоеточия на символ подчёркивания
        # для использования в качестве callback
        time_callback = "_".join(time.split(":"))
        inline_kb.insert(InlineKeyboardButton(time, callback_data=time_calendar_callback.new(
            action="time_choice", time=time_callback)))
    # Предпоследняя строка - возврат к выбору даты
    inline_kb.row()
    inline_kb.insert(InlineKeyboardButton(text=f"{emojis.right_arrow_curving_left} Вернуться к выбору даты",
                                          callback_data=time_calendar_callback.new(
                                              action="step_back", time=0)))
    # Предпоследняя строка - возврат в главное меню
    inline_kb.row()
    inline_kb.insert(InlineKeyboardButton(text=f"{emojis.home} Главное меню",
                                          callback_data=time_calendar_callback.new(
                                              action="backtotop", time=0)))
    return inline_kb
