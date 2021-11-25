from aiogram import types
from aiogram.dispatcher.storage import FSMContext

from keyboards.inline.callback_datas import (
    backtotop_callback,
    cancel_callback,
    office_detail_callback,
    time_calendar_callback,
    type_window_callback,
    unsubscribe_callback,
)
from keyboards.inline.main import mainmenu
from loader import dispatcher
from states.case_status import CaseStatusQuestions


@dispatcher.callback_query_handler(backtotop_callback.filter(action="backtotop"))
@dispatcher.callback_query_handler(office_detail_callback.filter(action="backtotop"))
@dispatcher.callback_query_handler(time_calendar_callback.filter(action="backtotop"))
@dispatcher.callback_query_handler(unsubscribe_callback.filter(action="backtotop"))
@dispatcher.callback_query_handler(type_window_callback.filter(action="backtotop"))
@dispatcher.callback_query_handler(cancel_callback.filter(action="cancel"))
@dispatcher.callback_query_handler(state=CaseStatusQuestions.Q1)
async def backtotop(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("Добро пожаловать в главное меню, вот что здесь есть:")
    await call.message.edit_reply_markup(reply_markup=mainmenu)
    await state.finish()
