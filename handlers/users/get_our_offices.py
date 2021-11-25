from itertools import islice

from aiogram import types
from aiogram.dispatcher.filters import Text

from filters.via_bot import ViaBot
from keyboards.inline.callback_datas import office_detail_callback
from loader import dispatcher, db_connector, bot_id, emojis


@dispatcher.inline_handler(text="offices")
async def select_district_command(query: types.InlineQuery):
    offset = int(query.offset) if query.offset else 0
    results_inline_query = []
    offices = await db_connector.get_offices_info()
    choice_office_text = "<b>Выбран офис: </b>"
    for office in islice(offices, offset, offset + 50):
        office_small_name = office.get("officeNameSmall")
        address = office.get("mfcAddress")
        results_inline_query.append(types.InlineQueryResultArticle(
            id=office.get("mfcId"),
            title=office_small_name,
            input_message_content=types.InputTextMessageContent(message_text=f"{choice_office_text}{office_small_name}"),
            description=address
        ))
    if len(results_inline_query) < 50:
        # Результатов больше не будет, next_offset пустой
        await query.answer(results_inline_query, is_personal=True, next_offset=None, cache_time=0)
    else:
        # Ожидаем следующую порцию данных
        await query.answer(results_inline_query, is_personal=True, next_offset=str(offset + 50), cache_time=0)
    await query.answer(results_inline_query, cache_time=0)


@dispatcher.message_handler(Text(startswith="Выбран офис: "), ViaBot(bot_id))
async def get_detail_office(message: types.Message):
    offices = await db_connector.get_offices_info()
    # Обрезать текст "Выбран офис: " выбора офиса из списка словарей
    office_small_name = message.text[13:]
    for office in offices:
        if office.get("officeNameSmall") == office_small_name:
            msg = [
                f"<b>Номер телефона:</b> <code>{office.get('phoneNumber')}</code>",
                f"<b>Сайт</b>: {office.get('website')}",
                f"<b>E-mail:</b> {office.get('mfcEmail')}",
            ]
            queue_id = office.get("queueId")
            officemenu = types.InlineKeyboardMarkup(row_width=1)
            officemenu.insert(types.InlineKeyboardButton(text=f"{emojis.clipboard} Предварительная запись",
                                                         callback_data=office_detail_callback.new(
                                                             action="pre_entry", queue_id=queue_id)))
            officemenu.insert(types.InlineKeyboardButton(text=f"{emojis.home} Главное меню",
                                                         callback_data=office_detail_callback.new(
                                                             action="backtotop", queue_id=0)))
            await message.answer("\n".join(msg), reply_markup=officemenu)
            break
