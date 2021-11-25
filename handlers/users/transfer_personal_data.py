from aiogram import types
from aiogram.dispatcher.filters import ContentTypeFilter, Text
from aiogram.dispatcher.storage import FSMContext

from keyboards.default.cancel import cancel_def_menu
from keyboards.default.get_contact import get_contact_def_menu
from keyboards.inline.backtotop import backtotopmenu
from keyboards.inline.callback_datas import main_callback, unsubscribe_callback
from keyboards.inline.main import mainmenu
from keyboards.inline.unsubscribe import unsubscribemenu
from loader import dispatcher, db_connector, emojis
from states.transfer_personal_data import TransferPersonalDataQuestions
from utils import misc


@dispatcher.callback_query_handler(main_callback.filter(action="transmit_personal_data"))
async def surname_and_mobile_choice(call: types.CallbackQuery):
    msg = [
        "Чтобы вы могли пользоваться сервисом предварительной записи в электронную очередь, "
        "сообщите мне свои персональные данные.",
        "",
        "Поделитесь номером телефона, нажав на кнопку ниже, в меню, под клавиатурой. "
        "Затем я спрошу ваши фамилию, имя и отчество.",
        "",
        "Если хотите удалить свои персональные данные из базы бота, то нажмите соответствующую кнопку "
        "и я удалю их.",
        "",
        f"Если хотите отменить действие, нажмите на кнопку {emojis.home} <b>Главное меню</b>."
    ]
    await call.answer()
    await call.message.delete()
    await call.message.answer("\n".join(msg), reply_markup=get_contact_def_menu)
    await TransferPersonalDataQuestions.first()


@dispatcher.message_handler(content_types=types.ContentTypes.CONTACT, state=TransferPersonalDataQuestions.Q1)
async def get_mobile(message: types.Message, state: FSMContext):
    mobile = f"+{message.contact.phone_number.strip('+')}"
    await state.update_data(mobile=mobile)
    await message.answer("Номер телефона получен!", reply_markup=types.ReplyKeyboardRemove())
    msg = [
        "Теперь введите фамилию, имя и отчество.",
    ]
    await message.answer("\n".join(msg), reply_markup=cancel_def_menu)
    await TransferPersonalDataQuestions.next()


@dispatcher.message_handler(Text(f"{emojis.cross_mark} Отмена"), state=TransferPersonalDataQuestions.Q2)
async def cancel_personal_data_entry(message: types.Message, state: FSMContext):
    await message.answer("Вы отменили ввод своих персональных данных.",
                         reply_markup=types.ReplyKeyboardRemove())
    await message.answer("Возвращаемся в главное меню?", reply_markup=backtotopmenu)
    await state.finish()


@dispatcher.message_handler(ContentTypeFilter(types.ContentType.TEXT), state=TransferPersonalDataQuestions.Q2)
async def get_surname(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    tg_user_id = message.from_user.id
    personal_data = misc.get_personal_data_from_string(message.text)
    if personal_data:
        mobile = state_data.get("mobile")
        # Записать персональные данные пользователя в базу данных бота
        await db_connector.add_or_replace_user(tg_user_id=tg_user_id,
                                               surname=personal_data.surname,
                                               name=personal_data.name,
                                               middlename=personal_data.middlename,
                                               mobile=mobile)
        msg = [
            "Ваши личные данные собраны и записаны в базу бота, спасибо.",
            "",
            f"Теперь вы можете записаться в электронную очередь. {emojis.robot}",
        ]
        await message.answer("\n".join(msg), reply_markup=types.ReplyKeyboardRemove())
        await message.answer("Если вы передумали и хотите удалить свои данные из базы бота, "
                             "то нажмите на кнопку ниже.", reply_markup=unsubscribemenu)
    else:
        msg = [
            f"{emojis.warning} Вы передали текст не похожий на фамилию имя и отчество. Попробуйте ещё раз",
        ]
        await message.answer("\n".join(msg), reply_markup=types.ReplyKeyboardRemove())
        await message.answer("Возвращаемся в главное меню?", reply_markup=backtotopmenu)
    await state.finish()


@dispatcher.message_handler(Text(f"{emojis.cross_mark} Отписаться от получения статусов"),
                            state=TransferPersonalDataQuestions.Q1)
async def unsubscribe_statuses(message: types.Message, state: FSMContext):
    tg_user_id = message.from_user.id
    if await db_connector.get_user_info(tg_user_id):
        await db_connector.delete_user(tg_user_id)
        msg = "Вы отменили получение оповещений об изменении статусов дел."
    else:
        msg = "Ваших данных нет в базе бота, нечего удалять."
    await message.answer(msg, reply_markup=types.ReplyKeyboardRemove())
    await message.answer("Возвращаемся в главное меню?", reply_markup=backtotopmenu)
    await state.finish()


@dispatcher.message_handler(Text(f"{emojis.home} Главное меню"), state=TransferPersonalDataQuestions.Q1)
async def backtotop_default_menu(message: types.Message, state: FSMContext):
    await message.answer("Вы отменили ввод своих персональных данных.",
                         reply_markup=types.ReplyKeyboardRemove())
    await message.answer("Добро пожаловать в главное меню, вот что здесь есть:", reply_markup=mainmenu)
    await state.finish()


@dispatcher.callback_query_handler(unsubscribe_callback.filter(action="cancel"))
async def unsubscribe_cancel(call: types.CallbackQuery):
    tg_user_id = call.from_user.id
    if await db_connector.get_user_info(tg_user_id):
        await db_connector.delete_user(tg_user_id)
        await call.answer("Вы удалили свои фамилию, имя, отчетство и номер телефоона из базы бота.", show_alert=True)
    else:
        await call.answer("Ваших данных нет в базе бота, нечего удалять.", show_alert=True)
    await call.message.edit_text("Добро пожаловать в главное меню, вот что здесь есть:")
    await call.message.edit_reply_markup(reply_markup=mainmenu)
