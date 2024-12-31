import asyncio
import logging
from keyboards import inline
from loader import dp, bot
from aiogram import Dispatcher, Bot
from utils import API
from data import config
from db import mysql
from utils.API_X import delete_user_x, modify_user_status_x


async def enable_disable_config(list_user_device, status):
    for user_device in list_user_device:
        try:
            print(await API.enable_disable_config(config.dict_server[user_device['number_server']]['url'], config.dict_server[user_device['number_server']]['password'], user_device['id_server'], status))
        except Exception as e:
            logging.error(f'{user_device} Ошибка при остановке {e}')


async def calculate_summa(count_config, sum_tariff):
    return count_config * sum_tariff


async def check_balance_and_debits_money(dp: Dispatcher):
    count_stop_conf = 0
    count_del_conf = 0
    """проверка конфигов"""
    list_configs = await mysql.get_all_configs_and_users()
    for conf in list_configs:
        if conf['friend']:
            continue
        balance = await mysql.get_balance(conf['user_id'])
        if balance['balance'] >= conf['sum_tariff']:
            try:
                await mysql.un_balance_and_get_user_info(conf['user_id'], conf['sum_tariff'])
            except Exception as e:
                logging.exception(f"Ошибка при попытке списать оплату за конфиг {conf['user_id']}: {e}")
        else:
            if conf['warn'] < 3:
                if conf['protocol'] == 1:
                    await enable_disable_config([conf], 'disable')
                    count_stop_conf += 1
                else:
                    await modify_user_status_x(conf['config_name'], 'disabled', conf['number_server'])
                    count_stop_conf += 1
                await mysql.set_warn_and_get_user_info(conf['user_id'], 1)
                try:
                    await bot.send_message(conf['user_id'], f"⛔️ Ваш конфигурационный файл <b>{conf['config_name']}</b> приостановлен.",
                                           reply_markup=inline.get_keyboard_up_balance_apshedule())
                except Exception as e:
                    logging.error(f"Пользователь {conf['user_id']} заблокировал бота")
            else:
                if conf['protocol'] == 1:
                    result = await API.delete_peer(config.dict_server[conf['number_server']]['url'], config.dict_server[conf['number_server']]['password'], conf['id_server'])
                    count_del_conf += 1
                    await mysql.delete_peer(conf['config_name'])
                else:
                    result = await delete_user_x(conf['config_name'], conf['number_server'])
                    count_del_conf += 1
                    await mysql.delete_peer(conf['config_name'])
                try:
                    await bot.send_message(conf['user_id'], f"🚫 Ваш конфигурационный файл <b>{conf['config_name']}</b> был удален.",
                                           reply_markup=inline.get_keyboard_up_balance_apshedule())
                except Exception as e:
                    logging.error(f"Пользователь {conf['user_id']} заблокировал бота")
    await bot.send_message(config.ADMINS_CHAT, f'✅ Проверка оплаты конфигов завершена.\n\nОстановлено: {count_stop_conf}\nУдалено: {count_del_conf}')