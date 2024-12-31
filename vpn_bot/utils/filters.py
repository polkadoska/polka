from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from data import config


class IsAdminChatFilter(BoundFilter):
    key = 'is_admin_chat'

    def __init__(self, is_admin_chat):
        self.is_admin_chat = is_admin_chat

    async def check(self, message: types.Message):
        chat_id = message.sender_chat.id
        return str(chat_id) in config.ADMINS_CHAT