from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

import config

# Проверка на админа
class IsAdmin(BoundFilter):
    async def check(self, message: types.Message):
        return message.from_user.id in config.admin_id
