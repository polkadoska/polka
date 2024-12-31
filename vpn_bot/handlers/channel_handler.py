import asyncio
from datetime import date
from aiogram.dispatcher.filters import Text, Command
from aiogram.dispatcher import FSMContext
from aiogram import types
from loader import dp, bot
from states import *
from utils import API, apschedule, filters
import logging
from utils import apschedule
from data import config
from db import mysql
from utils.API_X import delete_user_x, modify_user_status_x


@dp.channel_post_handler(filters.IsAdminChatFilter(is_admin_chat=True), Command('help'))
async def command_help(message: types.Message):
    text = """/set_friend user_id status(0, 1)
/set_balance user_id balance - добавить баланс
/un_balance user_id balance - убавить баланс
/stop_user user_id - остановить все конфиги пользователя
/remove_user user_id - удалить все конфиги пользователя и его самого
/stat - статистика
/set_price PRICE(число вместо PRICE)"""
    await message.answer(text)


# поставить статус жабы
@dp.channel_post_handler(filters.IsAdminChatFilter(is_admin_chat=True), Command('set_friend'))
async def command_set_friends(message: types.Message):
    try:
        command, user_id, status = message.text.split()
        status = int(status)
        await mysql.set_friend(user_id, status)
        if status == 1:
            await bot.send_message(chat_id=user_id, text="Вам установлен статус: Free")
            await message.answer(f'Вы установили пользователю {user_id}, статус: Free')
        else:
            await bot.send_message(chat_id=user_id, text="Вам убрали статус: Free")
            await message.answer(f'Вы убрали пользователю {user_id}, статус: Free')
    except Exception as e:
        logging.exception(e)


# сделать рассылку пользователям
@dp.channel_post_handler(filters.IsAdminChatFilter(is_admin_chat=True), Command('newswhere'))
async def command_news(message: types.Message):
    count = 0
    text = message.text[13:]
    number_server = message.text[11:12]
    users = await mysql.get_users_info_where(int(number_server))
    for user in users:
        try:
            await bot.send_message(chat_id=user['user_id'], text=text)
        except Exception as e:
            count += 1
            logging.error(f"user_id: {user['user_id']} Ошибка при рассылке сообщения {e}")
    await message.answer(f'Рассылка всем пользователям успешно завершена\nНе получилось отправить {count} пользователям')


@dp.channel_post_handler(filters.IsAdminChatFilter(is_admin_chat=True), Command('set_balance'))
async def command_set_balance(message: types.Message):
    try:
        command, user_id, balance = message.text.split()
        await mysql.set_balance_and_get_user_info(user_id, int(balance))
        await message.answer(f'Пополнили баланс пользователя {user_id} на {balance}')
        await bot.send_message(chat_id=user_id, text=f'Ваш баланс пополнен на {balance} рублей')
    except Exception as e:
        await message.answer(f'🚫 Ошибка: {e}')


@dp.channel_post_handler(filters.IsAdminChatFilter(is_admin_chat=True), Command('un_balance'))
async def command_un_balance(message: types.Message):
    try:
        command, user_id, balance = message.text.split()
        await mysql.un_balance_and_get_user_info(user_id, int(balance))
        await message.answer(f'Списали с баланса {user_id} пользователя {balance}')
    except Exception as e:
        await message.answer(f'🚫 Ошибка: {e}')


@dp.channel_post_handler(filters.IsAdminChatFilter(is_admin_chat=True), Command('re'))
async def command_re(message: types.Message):
    try:
        command, user_id, *text = message.text.split()
        text.append('\n\nС уважением Администрация сервиса\n<b>/start</b> - вернуться личный кабинет')
        await bot.send_message(chat_id=user_id, text=' '.join(text))
        await message.answer('Отправлено')
    except Exception as e:
        await message.answer(f'🚫 Ошибка: {e}')


@dp.channel_post_handler(filters.IsAdminChatFilter(is_admin_chat=True), Command('stop_user'))
async def command_stop_user(message: types.Message):
    try:
        command, user_id = message.text.split()
        list_user_device = await mysql.get_user_device(user_id)
        for conf in list_user_device:
            try:
                await apschedule.enable_disable_config([conf], 'disable')
            except Exception as e:
                pass
            try:
                await modify_user_status_x(conf['config_name'], 'disabled', conf['number_server'])
            except Exception as e:
                pass
        await message.answer(f'Пользователь {user_id} остановлен')
    except Exception as e:
        await message.answer(f'🚫 Ошибка: {e}')


@dp.channel_post_handler(filters.IsAdminChatFilter(is_admin_chat=True), Command('go_user'))
async def command_go_user(message: types.Message):
    try:
        command, user_id = message.text.split()
        list_user_device = await mysql.get_user_device(user_id)
        for conf in list_user_device:
            try:
                await apschedule.enable_disable_config([conf], 'enable')
            except Exception as e:
                pass
            try:
                await modify_user_status_x(
                    conf['config_name'], 
                    'active', 
                    conf['number_server']
                    )
            except Exception as e:
                pass
        await message.answer(f'Пользователь {user_id} разблокирован')
    except Exception as e:
        await message.answer(f'🚫 Ошибка: {e}')



@dp.channel_post_handler(filters.IsAdminChatFilter(is_admin_chat=True), Command('remove_user'))
async def command_remove_user(message: types.Message):
    command, user_id = message.text.split()
    list_user_device = await mysql.get_user_device(user_id)
    for user_device in list_user_device:
        try:
            result = await API.delete_peer(config.dict_server[user_device['number_server']]['url'], config.dict_server[user_device['number_server']]['password'], user_device['id_server'])
            if result:
                await mysql.delete_peer(user_device['config_name'])
            await asyncio.sleep(2)
        except Exception as e:
            await message.answer(f'🚫 Ошибка: {e}')
            logging.error(f'{user_device} Ошибка при удалении {e}')
        try:
            await delete_user_x(
                user_device['config_name'],
                user_device['number_server'])
            await mysql.delete_peer(user_device['config_name'])
        except Exception as e:
            logging.error(f'{user_device} Ошибка при удалении {e}')


@dp.channel_post_handler(filters.IsAdminChatFilter(is_admin_chat=True), content_types=types.ContentTypes.DOCUMENT)
async def proccess_work_with_receipt(message: types.Message):
    try:
        if message.caption.startswith('/receipt'):
            command, user_id = message.caption.split()
            photo = message.document.file_id
            await bot.send_document(chat_id=user_id,
                                    document=photo,
                                    caption='Высылаем вам чек, по вашему запросу.')
    except Exception as e:
        await message.answer(f'🚫 Ошибка: {e}')


@dp.channel_post_handler(filters.IsAdminChatFilter(is_admin_chat=True), Command('stat'))
async def command_stat(message: types.Message):
    data = await mysql.get_stat()
    text = f"""📊 Статистика {date.today()}

Всего пользователей: <b>{data['count_users']}</b>
Всего конфигов: <b>{data['count_config']}</b>"""
    for i, serv in config.dict_server.items():
        text += f"\n{i} сервер ({serv['country']}): <b>{data[f'count_server_{i}']}</b>"
    await message.answer(text)


@dp.channel_post_handler(filters.IsAdminChatFilter(is_admin_chat=True), Command('set_price'))
async def command_set_price(message: types.Message):
    comand, price = message.text.split()
    await mysql.set_price(int(price))
    await message.answer(f'Цена за конфиг установлена на {price} руб')