import logging
from aiogram.dispatcher.filters import Text
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageNotModified
from loader import dp, bot
from keyboards import inline
from states import *
from db import mysql
from utils.message_utils import *


@dp.callback_query_handler(Text(equals='admin:out'), state=user_state.UserStateGroup.admin)
async def callback_admin_out(callback: types.CallbackQuery, state: FSMContext):
    new_text = "Вы вышли из панели администратора"
    await edit_message(callback.message, new_text, reply_markup=None)
    await state.finish()


@dp.callback_query_handler(Text(equals='admin:message'), state=user_state.UserStateGroup.admin)
async def callback_admin_message(callback: types.CallbackQuery, state: FSMContext):
    await edit_message(callback.message, "Введите текст для рассылки (пока что только текст)")
    await state.set_state(user_state.UserStateGroup.admin_message.state)


@dp.callback_query_handler(Text(equals='admin:go_message'), state=user_state.UserStateGroup.admin)
async def callback_admin_go_message(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        admin_message_text = data['admin_message_text']
    await edit_message(callback.message, "Рассылка началась", reply_markup=inline.get_keyboard_admin())
    count = 0
    count_error = 0
    list_users = await mysql.get_all_users_info()
    for user in list_users:
        try:
            await bot.send_message(chat_id=user['user_id'], text=admin_message_text)
            count += 1
        except Exception as e:
            count_error += 1
            logging.exception(e)
    await callback.message.answer(f"Рассылка завершена\nОтправлено: {count}\nНе отправилось: {count_error}")


@dp.callback_query_handler(Text(equals='admin:cancel_message'), state=user_state.UserStateGroup.admin)
async def callback_admin_cancel_message(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['admin_message_text'] = None
    await callback.message.answer('Добро пожаловать в панель администратора', reply_markup=inline.get_keyboard_admin())


@dp.callback_query_handler(Text(equals='admin:video'), state=user_state.UserStateGroup.admin)
async def callback_admin_video(callback: types.CallbackQuery, state: FSMContext):
    await edit_message(callback.message, "Пришлите видео")