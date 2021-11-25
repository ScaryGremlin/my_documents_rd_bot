from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class ViaBot(BoundFilter):
    def __init__(self, bot_id: int):
        self.__bot_id = bot_id

    async def check(self, message: types.Message) -> bool:
        if message.via_bot:
            if message.via_bot.id == self.__bot_id:
                return True
        return False
