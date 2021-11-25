import sqlite3
from json import loads
from typing import Iterable, Any

import aiosqlite

from data import creds


class DBConnector:
    """
    Класс взаимодействия с базой данных
    """
    def __init__(self, db_file_name: str = creds.DB_FILE_NAME):
        self.__db_file_name = db_file_name

    async def __execute_query(self, text_query: str = None, params: Iterable[Any] = None) -> Iterable[sqlite3.Row]:
        """
        Выполнить SQL-запрос
        :param text_query: Текст запроса
        :param params: Итерируемый объект с перечислением параметров запроса
        :return: Результат запроса
        """
        async with aiosqlite.connect(self.__db_file_name) as db_conn:
            cursor = await db_conn.cursor()
            await cursor.execute(text_query, params)
            await db_conn.commit()
            return await cursor.fetchall()

    async def create_users_table(self) -> None:
        """
        Создать таблицу с данными пользоватеей в базе данных бота
        :return:
        """
        query = """CREATE TABLE IF NOT EXISTS users (
                        tg_user_id INTEGER UNIQUE NOT NULL,
                        surname TEXT NOT NULL,
                        name TEXT NOT NULL,
                        middlename TEXT NOT NULL,
                        mobile TEXT NOT NULL,
                        cases JSON
                    )"""
        await self.__execute_query(query)

    async def create_offices_table(self) -> None:
        """

        :return:
        """
        query = """CREATE TABLE IF NOT EXISTS offices (
                                id INTEGER UNIQUE NOT NULL,
                                offices JSON NOT NULL
                            )"""
        await self.__execute_query(query)

    async def add_or_replace_user(self, tg_user_id: int,
                                  surname: str, name: str, middlename: str,
                                  mobile: str, cases: dict = None) -> None:
        """
        Добавить пользователя в базу данных бота.
        Если пользовате уже есть в базе, то обновить его.
        :param tg_user_id: ID пользователя в Telegram
        :param surname: Фамилия пользователя
        :param name: Имя пользователя
        :param middlename: Отчество пользователя
        :param mobile: Мобильный телефон пользователя
        :param cases: Дела пользователя в формате json
        :return:
        """
        query = """INSERT OR REPLACE INTO users 
                    (tg_user_id, surname, name, middlename, mobile, cases) 
                    VALUES (?, ?, ?, ?, ?, ?)
                """
        params = (tg_user_id, surname, name, middlename, mobile, cases)
        await self.__execute_query(query, params)

    async def get_user_info(self, tg_user_id: int) -> Iterable[sqlite3.Row]:
        """
        Получить информацию о пользователе из базы данных бота.
        Фамилию, мобильный теефон и дела пользователя в формате json
        :param tg_user_id: ID пользователя в Telegram
        :return: Фамилия, имя, отчество и мобильный телефон пользователя
        """
        query = "SELECT surname, name, middlename, mobile FROM users WHERE tg_user_id = ?"
        params = (tg_user_id, )
        return await self.__execute_query(query, params)

    async def delete_user(self, tg_user_id: int) -> Iterable[sqlite3.Row]:
        """
        Удалить пользователя из базы данных бота
        :param tg_user_id: ID пользователя в Telegram
        :return:
        """
        query = "DELETE FROM users WHERE tg_user_id = ?"
        params = (tg_user_id, )
        return await self.__execute_query(query, params)

    async def select_all_users(self) -> Iterable[sqlite3.Row]:
        """
        Выбрать всех пользователей из базы данных бота
        :return: Кортеж с данными всех пользователей
        """
        query = "SELECT * FROM users"
        return await self.__execute_query(query)

    async def add_offices_info(self, offices: list) -> None:
        """

        :param offices:
        :return:
        """
        query = "INSERT OR REPLACE INTO offices (id, offices) VALUES (?, ?)"
        params = (1, offices)
        await self.__execute_query(query, params)

    async def get_offices_info(self) -> list:
        """

        :return:
        """
        query = "SELECT offices FROM offices WHERE id = 1"
        offices = await self.__execute_query(query)
        return loads(offices[0][0])
