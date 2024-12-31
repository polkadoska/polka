import logging
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram import types
from loader import dp, bot
from keyboards import inline, reply
from states import *
from states import user_state
from db import mysql
from data.config import ADMIN_PASSWORD
# from utils.message_utils import *


@dp.message_handler(commands=['admin'], state="*")
async def show_admin_panel(message: types.Message, state: FSMContext):
    if message.text[7:] == ADMIN_PASSWORD:
        await message.answer('Добро пожаловать в панель администратора', reply_markup=inline.get_keyboard_admin())
        await state.set_state(user_state.UserStateGroup.admin.state)
    else:
        await message.answer('Пароль не верный')


@dp.message_handler(state=user_state.UserStateGroup.admin)
async def admin_message_text(message: types.Message, state: FSMContext):
    await message.answer('Добро пожаловать в панель администратора', reply_markup=inline.get_keyboard_admin())


@dp.message_handler(state=user_state.UserStateGroup.admin_message)
async def admin_message_text(message: types.Message, state: FSMContext):
    message_text = message.html_text
    async with state.proxy() as data:
        data['admin_message_text'] = message_text 
    await message.answer(message_text, reply_markup=inline.get_keyboard_admin_check_message())
    await state.set_state(user_state.UserStateGroup.admin.state)


@dp.message_handler(content_types=types.ContentTypes.VIDEO, state=user_state.UserStateGroup.admin)
async def get_admin_video(message: types.Message):
    await message.answer(message.video.file_id)
