from datetime import datetime
from typing import Union

from data.types import Person


def get_personal_data_from_string(raw_string: str) -> Union[Person, None]:
    """
    Получить персональные данные - фамилию, имя и отчество пользователя из сырой строки.
    :param raw_string: Строка сырых данных
    :return: Кортеж с фамилией, именем и отчеством.
    """
    try:
        surname, name, middlename = raw_string.split()
    except ValueError:
        return None
    return Person(surname.capitalize(), name.capitalize(), middlename.capitalize())


def get_formatted_pre_entry(raw_pre_entry: list) -> dict:
    """

    :param raw_pre_entry:
    :return:
    """
    formatted_pre_entry = {}
    for day in raw_pre_entry:
        date = datetime.strptime(day.get("date_number"), "%d.%m.%Y").date()
        formatted_pre_entry.update({date: day.get("time")})
    return formatted_pre_entry
