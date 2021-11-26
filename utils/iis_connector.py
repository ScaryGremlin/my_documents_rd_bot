from collections import namedtuple
from typing import Optional

import aiohttp

from data.types import Emoji, Urls
from json import dumps, JSONEncoder


class IisConnector:
    """
    Класс взаимодействия с ИИС
    """

    Response = namedtuple("Response", ["status", "data"])

    def __init__(self):
        """

        """
        self.__http_session = aiohttp.ClientSession()
        self.__units_list = []
        self.__unit_schedule = {}
        self.__emojis = Emoji()
        self.__urls = Urls()

    async def __api_request(self, method: str, param_url: str,
                            param: str = None, payload=None,
                            headers: dict = None) -> Response:
        """

        :param method:
        :param param_url:
        :param param:
        :param payload:
        :param headers:
        :return:
        """
        url = f"{self.__urls.iis_api_base}{param_url.format(case_number=param)}"
        if method == "get":
            async with self.__http_session.get(url, params=payload) as response:
                print(response.real_url)
                return self.Response(response.status, await response.json())
        elif method == "post":
            async with self.__http_session.post(url, data=payload, headers=headers) as response:
                print(response.real_url)
                return self.Response(response.status, await response.json())

    async def case_status(self, case_number: str):
        """

        :param case_number:
        :return:
        """
        response = await self.__api_request(method="get", param_url=self.__urls.iis_api_case_status, param=case_number)
        return self.Response(response.status, response.data)

    async def units_list(self) -> list:
        """

        :return:
        """
        response = await self.__api_request(method="get", param_url=self.__urls.iis_api_units_list)
        if response.status == 200:
            return response.data

    async def get_pre_entry(self, queue_id: int) -> Response:
        """

        :return:
        """
        payload = {"queueId": queue_id}
        response = await self.__api_request(method="get",
                                            param_url=self.__urls.iis_api_preregistration_date,
                                            payload=payload)
        return self.Response(response.status, response.data)

    async def enqueue(self, queue_id: int,
                      surname: str, name: str, middlename: str, mobile: str,
                      service: int, date: str, time: str):
        """

        :param queue_id:
        :param surname:
        :param name:
        :param middlename:
        :param mobile:
        :param service:
        :param date:
        :param time:
        :return:
        """
        payload = {
            "fio": f"{surname} {name} {middlename}",
            "phone": mobile,
            "service": service,
            "date": date,
            "time": time,
        }
        headers = {
            "Content-Type": "application/json"
        }
        response = await self.__api_request(method="post",
                                            param_url=f"{self.__urls.iis_api_preregistration_add}/{queue_id}",
                                            payload=dumps(payload),
                                            headers=headers)
        return self.Response(response.status, response.data)
