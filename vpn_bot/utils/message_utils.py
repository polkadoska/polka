from aiogram.utils.exceptions import MessageNotModified
from contextlib import suppress
from aiogram import types


async def edit_message(message: types.Message, new_text: str, reply_markup=None):
    with suppress(MessageNotModified):
        await message.edit_text(new_text, reply_markup=reply_markup, parse_mode=types.ParseMode.HTML)