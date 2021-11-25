from aiogram import types
from aiogram.dispatcher.filters import ContentTypeFilter
from aiogram.dispatcher.storage import FSMContext

from keyboards.inline.backtotop import backtotopmenu
from keyboards.inline.callback_datas import main_callback
from keyboards.inline.cancel import cancelmenu
from loader import dispatcher, emojis, iis_connector
from states.case_status import CaseStatusQuestions


@dispatcher.callback_query_handler(main_callback.filter(action="case_status"))
async def case_status_choice(call: types.CallbackQuery):
    await call.message.edit_text("Введите номер дела:")
    await call.message.edit_reply_markup(reply_markup=cancelmenu)
    await CaseStatusQuestions.first()


@dispatcher.message_handler(ContentTypeFilter(types.ContentType.TEXT), state=CaseStatusQuestions.Q1)
async def get_case_info_by_num(message: types.Message, state: FSMContext):
    case_number = message.text
    response = await iis_connector.case_status(case_number)
    if response.status == 200:
        msg = [
            f"<b>Заявитель:</b> <code>{response.data.get('customerName')}</code>",
            f"<b>Услуга:</b> <code>{response.data.get('servicesName')}</code>",
            f"<b>Статус дела:</b> <code>{response.data.get('statusName')}</code>",
        ]
    else:
        msg = [
            f"{emojis.warning} Ошибка получения статуса дела.",
            f"<code>{response.data}</code>",
        ]
    await message.answer("\n".join(msg))
    await message.answer("Возвращаемся в главное меню?", reply_markup=backtotopmenu)
    await state.finish()
