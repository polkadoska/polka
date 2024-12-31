import logging
from aiogram.dispatcher.filters import Text
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageNotModified
from loader import dp, bot
from keyboards import inline
from states import *
from utils import yoo
from utils.message_utils import edit_message
from db import mysql
import re


@dp.callback_query_handler(Text(equals='up_balance'), state="*")
async def callback_up_balance(callback: types.CallbackQuery):
    await callback.answer(None)
    new_text = "Выберете способ оплаты сервиса"
    await edit_message(callback.message, new_text, reply_markup=inline.get_keyboard_payment_methods())


@dp.callback_query_handler(Text(startswith='change_payment_method_'), state="*")
async def callback_change_payment_methods(callback: types.CallbackQuery):
    # await callback.answer('❌ Временно не доступно')
    try:
        await callback.answer(None)
    except Exception as e:
        logging.exception(f"Ошибка на ответ callback answer method{e}")
    change_payment = callback.data[22:]
    if change_payment == "rub":
        new_text = "Пополнение баланса является однократной операцией <b>(не подписка)</b>. Мы не имеем доступа к вашим личным и платежным данным"
        return await edit_message(callback.message, new_text, reply_markup=inline.get_keyboard_change_summa())


# оплата рублями деревянными
@dp.callback_query_handler(Text(startswith='change_summ_'), state="*")
async def callback_change_summa(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer(None)
    if callback.data[12:] == "other":
        new_text = "Введите сумму на которую хотите пополнить баланс\n\n<i>Она должна быть целым числом\nНапример: 1200</i>"
        await edit_message(callback.message, new_text, reply_markup=None)
        await state.update_data(type_change_payment=0)
        return await state.set_state(user_state.UserStateGroup.input_summa.state)
    summa = int(callback.data[12:])
    new_text = f"""Ваш баланс будет пополнен
на <b>{summa}</b> рублей.
<b>Спасибо, что пользуетесь сервисом</b>

⬇️
<b>Введите email для получения чека:</b>"""
    await state.update_data(summ_pay=summa)
    await edit_message(message=callback.message,
                       new_text=new_text,
                       reply_markup=inline.get_keyboard_not_receipt())
    await state.set_state(user_state.UserStateGroup.input_email.state)


@dp.message_handler(state=user_state.UserStateGroup.input_email)
async def handler_input_email(message: types.Message, state: FSMContext):
    if await is_valid_email(message.text):
        data_storage = await state.get_data()
        try:
            url = await yoo.payment_yandex(summa=int(data_storage.get('summ_pay')),
                                           user_id=message.from_user.id,
                                           email=message.text)
            await message.answer("Email принят, для оплаты перейдите по ссылке ниже ⬇️",
                                 reply_markup=inline.get_keyboard_link_to_payment(url))
            await state.finish()
        except Exception as e:
            await state.finish()
            await message.answer('Произошла ошибка, попробуйте еще раз.',
                                 reply_markup=inline.get_keyboard_profile())
    else:
        await message.answer('Email введен не корректно, попробуйте еще раз',
                             reply_markup=inline.get_keyboard_profile())


async def is_valid_email(text):
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    match = re.search(email_pattern, text)
    return bool(match)


@dp.callback_query_handler(Text(equals="skip_receipt"), state="*")
async def callback_skip_receipt(callback: types.CallbackQuery, state: FSMContext):
    data_storage = await state.get_data()
    try:
        url = await yoo.payment_yandex(summa=int(data_storage.get('summ_pay')),
                                       user_id=callback.from_user.id,
                                       email='yourmail@mail.ru')
        await edit_message(message=callback.message,
                           new_text="Для оплаты перейдите по ссылке ниже ⬇️",
                           reply_markup=inline.get_keyboard_link_to_payment(url))
        await state.finish()
    except Exception as e:
        await callback.message.answer('Произошла ошибка, попробуйте еще раз.',
                                      reply_markup=inline.get_keyboard_profile())
