from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram import types
from loader import dp, bot
from keyboards import inline
from states import *
from utils import get_profile, apschedule
from data import config
from db import mysql


# @dp.message_handler()
# async def name(message: types.Message):


@dp.message_handler(commands=['start'], state="*")
async def command_start_process(message: types.Message, state: FSMContext):
    await state.finish()
    referal = message.text[7:]
    if not await mysql.exist_user(message.from_user.id):
        data = await mysql.get_sum_tariff()
        await mysql.add_user(message.from_user.id, message.from_user.username, referal, sum_tariff=data['price'])
        first_text = "<b>Подробнее о нас:\n\n</b><b>Наш сервис</b> - это высококачественный VPN-сервис, который предоставляет надежные и безопасные услуги для вашей анонимности и безопасности в сети.\n\n Вся работа сервиса <b>полностью автоматизирована,</b>. Чтобы начать пользоваться VPN - потребуется всего пара минут.\n\nВыберите ваше устройство, мы в автоматическом режиме всё подготовим и отправим все необходимые инструкции! Сразу платить ничего не надо, <b>Вам  будет предоставлен бесплатный пробный период!</b>"

        await message.answer(first_text, reply_markup=inline.get_keyboard_change_device())
        return await state.set_state(user_state.UserStateGroup.change_device.state)
    # если юзер уже зарегистрован тогда выводим ему личный кабинет
    result = await mysql.get_user_info(str(message.from_user.id))
    text_profile = await get_profile.get_profile_data(result)
    await message.answer(text_profile, reply_markup=inline.get_keyboard_menu_profile())


@dp.message_handler(commands=['profile'], state="*")
async def command_profile_process(message: types.Message, state: FSMContext):
    result = await mysql.get_user_info(str(message.from_user.id))
    text_profile = await get_profile.get_profile_data(result)
    await message.answer(text_profile, reply_markup=inline.get_keyboard_menu_profile())


@dp.message_handler(commands=['apschedule'], state="*")
async def command_check_apchedule(message: types.Message):
    await apschedule.check_balance_and_debits_money(dp)


@dp.message_handler(state=user_state.UserStateGroup.input_summa)
async def input_summa_process(message: types.Message, state: FSMContext):
    try:
        summa = int(message.text)
        if summa < 20:
            return await message.answer('Сумма должна быть больше 20 рублей')
        user_info = await state.get_data()
        await message.answer(f'Ваш баланс будет пополнен на <b>{summa}</b> рублей', reply_markup=inline.get_keyboard_change_other_summa(user_info['type_change_payment'], summa))
        await state.finish()
    except Exception as e:
        await message.answer('Нужно ввести целое число\n\n<i>Например: 1200</i>')


@dp.message_handler(state=user_state.UserStateGroup.help.state)
async def command_help_user_state(message: types.Message, state: FSMContext):
    user_id = str(message.from_user.id)
    user_info = await mysql.get_user_info(user_id)
    text = f"""Вопрос от пользователя <code>{user_id}</code> @{message.from_user.username}
    
<b>{message.text}</b>

Что бы ответить ему введите:
<code>/re {user_id} </code> (текст)

<i>Баланс: {user_info['balance']}
Количество конфигов: {user_info['count_configs']}
Количество warn: {user_info['warn']}
</i>"""
    await bot.send_message(chat_id=config.ADMINS_CHAT, text=text)
    await state.finish()
    await message.answer('✅ Ваш вопрос успешно отправлен\n\n<b>/start</b> - вернуться в личный кабинет')