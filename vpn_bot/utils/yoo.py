import json
import logging
from data import config
from loader import bot
from keyboards import inline
from yookassa import Configuration, Payment
from db import mysql

from utils import apschedule
from utils.API_X import modify_user_status_x

Configuration.account_id = config.YOO_ACCOUNT_ID
Configuration.secret_key = config.YOO_SECRET_KEY


async def payment_yandex(summa: int, user_id: str, email: str):
    payment = Payment.create({
        "amount": {
            "value": summa,
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": config.RETURN_URL_YOOKASSA
        },
        "receipt": {
            "customer": {
                "email": email,
            },
            "tax_system_code": 2,
            "items": [
                {

                    "description": "Настройка доступа в интернет",
                    "quantity": "1",
                    "amount": {
                        "value": summa,
                        "currency": "RUB",
                    },
                    "vat_code": "1",
                },
            ]

        },
        "metadata": {"user_id": user_id},
        "capture": True,
        "description": "Настройка доступа в интернет"
    })
    try:
        payment_data = json.loads(payment.json())
        return payment_data['confirmation']['confirmation_url']
    except Exception as e:
        return config.RETURN_URL_YOOKASSA


async def success_pay(response):
    try:
        if response['event'] == "payment.succeeded":  # успешный платеж
            user_id = response['object']['metadata']['user_id']
            amount = int(response['object']['amount']['value'].split('.')[0])  # также ищем в словаре ответа сумму
            data = await mysql.get_sum_tariff()
            if amount > 99999:
                amount += amount / 100 * data['pay_bonus']
            user_info = await mysql.set_balance_and_get_user_info(user_id, amount)
            await bot.send_message(chat_id=user_id,
                                   text=f"✅ Ваш баланс <b>успешно</b> пополнен\n\nСумма платежа:<b>{amount}₽</b>",
                                   reply_markup=inline.get_keyboard_succsess_pay())
            if user_info['referal']:
                try:
                    referal_summa = int(amount / 100 * data['referal_procent'])
                    await mysql.set_referal_balance(user_info['referal'], referal_summa)
                    await bot.send_message(chat_id=user_info['referal'],
                                           text=f'<b>{referal_summa}</b> рублей.')
                except Exception as e:
                    logging.exception(e)
            list_user_device = await mysql.get_user_device(user_id)
            for conf in list_user_device:
                if conf['protocol'] == 1:
                    await apschedule.enable_disable_config([conf], 'enable')
                else:
                    await modify_user_status_x(
                        conf['config_name'],
                        'active',
                        conf['number_server'])
            await bot.send_message(chat_id=config.ADMINS_CHAT,
                                   text=f"💵 <code>{user_id}</code> пополнил баланс на <b>{amount}</b> рублей.")
    except Exception as e:
        logging.error(e)
