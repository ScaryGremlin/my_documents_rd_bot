from aiogram import types
from aiogram.dispatcher.storage import FSMContext

from keyboards.inline.backtotop import backtotopmenu
from keyboards.inline.bot_calendar import create_calendar, create_time_kb, process_calendar_selection
from keyboards.inline.callback_datas import (
    calendar_callback,
    office_detail_callback,
    time_calendar_callback,
    type_window_callback,
)
from keyboards.inline.type_window import typewindowmenu
from loader import db_connector, dispatcher, emojis, iis_connector
from utils import misc


@dispatcher.callback_query_handler(office_detail_callback.filter(action="pre_entry"))
async def pre_entry_choice(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    queue_id = callback_data.get("queue_id")
    tg_user_id = call.from_user.id
    user_info = await db_connector.get_user_info(tg_user_id)
    # Если персональные данные пользователя есть в базе бота, то запросить данные о предварительной записи
    if user_info:
        status_code, raw_pre_entry = await iis_connector.get_pre_entry(queue_id=queue_id)
        if status_code == 200:
            surname, name, middlename, mobile = user_info[0]
            # Записать персональные данные в state
            await state.update_data(queue_id=queue_id, surname=surname, name=name, middlename=middlename, mobile=mobile)
            pre_entry = misc.get_formatted_pre_entry(raw_pre_entry)
            pre_entry_dates = list(pre_entry.keys())
            await state.update_data(pre_entry=pre_entry)
            await call.answer()
            await call.message.edit_text(f"{emojis.calendar} Пожалуйста, выберете дату: ")
            await call.message.edit_reply_markup(reply_markup=create_calendar(pre_entry_dates=pre_entry_dates))
        elif status_code == 404:
            await call.answer()
            await call.message.edit_text(f"{emojis.warning} Нет мест для предварительной записи.")
            await call.message.edit_reply_markup(reply_markup=backtotopmenu)
        else:
            msg = [
                f"{emojis.warning} Что-то пошло не так.",
                f"<code>{status_code, raw_pre_entry}</code>",
            ]
            await call.answer()
            await call.message.edit_text("\n".join(msg))
            await call.message.edit_reply_markup(reply_markup=backtotopmenu)
    else:
        msg = [
            "Сначала сообщите боту свои персональные данные — фамилию, имя, отчество и номер телефона.",
            "Выберете в главноем меню соответствующий пункт.",
        ]
        await call.answer()
        await call.message.edit_text("\n".join(msg))
        await call.message.edit_reply_markup(reply_markup=backtotopmenu)


@dispatcher.callback_query_handler(calendar_callback.filter())
async def select_date(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    state_data = await state.get_data()
    pre_entry = state_data.get("pre_entry")
    pre_entry_dates = list(pre_entry.keys())
    is_selected, selected_date = await process_calendar_selection(call, callback_data, pre_entry_dates)
    if is_selected:
        await state.update_data(selected_date=selected_date)
        pre_entry_times = pre_entry.get(selected_date)
        msg = [
            f"{emojis.calendar} Выбрана дата: <code>{selected_date.strftime('%Y-%m-%d')}</code>",
            f"Свободное время для записи:",
        ]
        await call.answer()
        await call.message.edit_text("\n".join(msg))
        await call.message.edit_reply_markup(reply_markup=create_time_kb(pre_entry_times))


@dispatcher.callback_query_handler(time_calendar_callback.filter(action="step_back"))
async def step_back_time(call: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    pre_entry = state_data.get("pre_entry")
    pre_entry_dates = list(pre_entry.keys())
    await call.answer()
    await call.message.edit_text(f"{emojis.calendar} Пожалуйста, выберете дату: ")
    await call.message.edit_reply_markup(reply_markup=create_calendar(pre_entry_dates=pre_entry_dates))


@dispatcher.callback_query_handler((time_calendar_callback.filter(action="time_choice")))
async def select_time(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    selected_time = callback_data.get("time").replace("_", ":")
    await state.update_data(selected_time=selected_time)
    await call.answer()
    await call.message.edit_text("Пожалуйста, выберете тип окна: ")
    await call.message.edit_reply_markup(reply_markup=typewindowmenu)


@dispatcher.callback_query_handler(type_window_callback.filter(action="window_choice"))
async def select_type_window(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    state_data = await state.get_data()
    selected_date = state_data.get("selected_date")
    selected_time = state_data.get("selected_time")
    queue_id = state_data.get("queue_id")
    surname = state_data.get("surname")
    name = state_data.get("name")
    middlename = state_data.get("middlename")
    mobile = state_data.get("mobile")
    type_window = callback_data.get("type_window")
    # Записать пользователя в предварительную записать и вернуть ему номер талона или код ошибки
    response = await iis_connector.enqueue(queue_id=queue_id,
                                           surname=surname, name=name, middlename=middlename,
                                           mobile=mobile, service=type_window,
                                           date=selected_date.strftime("%Y.%m.%d"), time=selected_time)
    await call.answer()
    if response.status == 200:
        msg = [
            f"Вы записались на: <code>{selected_date}, {selected_time}</code>",
            f"Ваш номер в очереди: <code>{response.data.get('code')}</code>",
        ]
        await call.message.edit_text("\n".join(msg))
    else:
        msg = [
            f"{emojis.warning} Ошибка записи в очередь.",
            f"<code>{response.data}</code>",
        ]
        await call.message.edit_text("\n".join(msg))
    await call.message.answer("Возвращаемся в главное меню?", reply_markup=backtotopmenu)


@dispatcher.callback_query_handler(type_window_callback.filter(action="step_back"))
async def step_back_time(call: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    pre_entry = state_data.get("pre_entry")
    selected_date = state_data.get("selected_date")
    pre_entry_times = pre_entry.get(selected_date)
    msg = [
        f"{emojis.calendar} Выбрана дата: <code>{selected_date.strftime('%Y-%m-%d')}</code>",
        f"Свободное время для записи:",
    ]
    await call.answer()
    await call.message.edit_text("\n".join(msg))
    await call.message.edit_reply_markup(reply_markup=create_time_kb(pre_entry_times))
