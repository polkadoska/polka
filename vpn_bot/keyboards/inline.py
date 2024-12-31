from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from data.config import dict_server, dict_device, dict_tariff, dict_protocol


def get_keyboard_change_country(change=None) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    ikb.add(*[InlineKeyboardButton(value['country'] if key != change else f"✅ {value['country']}", callback_data=f"change_country_{key}") for key, value in dict_server.items()])
    ikb.add(InlineKeyboardButton('⬅️ Назад', callback_data='but_back_to:change_protocol'))
    return ikb


def get_keyboard_change_country_2(change=None) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    ikb.add(InlineKeyboardButton("✅ 🇬🇧 Великобритания" if change else "🇬🇧 Великобритания", callback_data=f"change_country_6"))
    ikb.add(InlineKeyboardButton('⬅️ Назад', callback_data='but_back_to:change_protocol'))
    return ikb


def get_keyboard_change_device(change=None) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    ikb.add(*[InlineKeyboardButton(value if key != change else f"✅ {value}", callback_data=f"change_device_{key}") for key, value in dict_device.items()])
    ikb.add(InlineKeyboardButton('⬅️ Назад', callback_data='back_to_profile'))
    return ikb


def get_keyboard_change_tariff(change=None) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    ikb.add(*[InlineKeyboardButton(value if key != change else f"✅ {value}", callback_data=f"change_tariff_{key}") for key, value in dict_tariff.items()])
    ikb.add(InlineKeyboardButton('⬅️ Назад', callback_data='but_back_to:change_device'))
    return ikb


def get_keyboard_change_protocol(change=None) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    ikb.add(*[InlineKeyboardButton(value if key != change else f"✅ {value}", callback_data=f"change_protocol_{key}") for key, value in dict_protocol.items()])
    ikb.add(InlineKeyboardButton('⬅️ Назад', callback_data='but_back_to:change_tariff'))
    return ikb


def get_keyboard_profile() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    ib1 = InlineKeyboardButton('Перейти в личный кабинет', callback_data='get_profile')
    ikb.add(ib1)
    return ikb


def get_keyboard_menu_profile() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    ib1 = InlineKeyboardButton('🔄 Обновить данные', callback_data='back_to_profile')
    ib2 = InlineKeyboardButton('💻 Мои устройства', callback_data='my_device')
    ib3 = InlineKeyboardButton('💳 Пополнить баланс', callback_data='change_payment_method_rub')
    ib5 = InlineKeyboardButton('🆘 Помощь', callback_data='help_system')
    ikb.add(ib1, ib2, ib3, ib5)
    return ikb


def get_keyboard_list_device(data: list) -> InlineKeyboardMarkup:
    """принимает список устрйоств юзера из базы данных возвращает их в видео клавиатуры с кнопками"""
    dict_device = {1: "📱",
               2: "📱",
               3: "💻",
               4: "💻"}

    ikb = InlineKeyboardMarkup(row_width=1)
    ikb.add(InlineKeyboardButton('➕ Добавить устройство', callback_data="add_device"))
    for device in data:
        ikb.add(InlineKeyboardButton(f"{dict_device[device['type_device']]} {device['config_name']} {dict_server[device['number_server']]['country'].split()[0]}", callback_data=f"change_device_info_{device['config_name']}"))
    ikb.add(InlineKeyboardButton('⬅️ Назад', callback_data="back_to_profile"))
    return ikb


def get_keyboard_controll_device(id: str) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    ib1 = InlineKeyboardButton('❌ Удалить', callback_data=f'del_{id}')
    ib2 = InlineKeyboardButton('⚙️ Показать конфиг', callback_data=f'conf_{id}')
    ib3 = InlineKeyboardButton('⬅️ Назад', callback_data='my_device')
    ikb.add(ib1, ib2, ib3)
    return ikb


def get_keyboard_hide_conf_file() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    ib1 = InlineKeyboardButton('⏏️ Скрыть', callback_data="hide_config")
    ikb.add(ib1)
    return ikb


def get_keyboard_payment_methods() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    ib1 = InlineKeyboardButton('🇷🇺 RUB', callback_data="change_payment_method_rub")
    ib2 = InlineKeyboardButton('💲 Криптовалюта', callback_data="change_payment_method_crypto")
    ib3 = InlineKeyboardButton('⬅️ Назад', callback_data='back_to_profile')
    ikb.add(ib1, ib3)
    return ikb


def get_keyboard_payment_methods_crypto() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    ib1 = InlineKeyboardButton('LTC', callback_data="change_payment_method_crypto_ltc")
    ib2 = InlineKeyboardButton('BTC', callback_data="change_payment_method_crypto_btc")
    ib3 = InlineKeyboardButton('⬅️ Назад', callback_data='back_to_profile')
    ikb.add(ib1, ib2, ib3)
    return ikb


def get_keyboard_change_summa() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=3)
    ib1 = InlineKeyboardButton('100₽', callback_data='change_summ_100')
    ib2 = InlineKeyboardButton('300₽', callback_data='change_summ_300')
    ib3 = InlineKeyboardButton('500₽', callback_data='change_summ_500')
    ib4 = InlineKeyboardButton('1000₽', callback_data='change_summ_1000')
    ib5 = InlineKeyboardButton('3000₽', callback_data='change_summ_3000')
    ib6 = InlineKeyboardButton('5000₽', callback_data='change_summ_5000')
    ib7 = InlineKeyboardButton('Другая сумма', callback_data='change_summ_other')
    ib8 = InlineKeyboardButton('⬅️ Отмена', callback_data='back_to_profile')
    ikb.add(ib1, ib2, ib3, ib4, ib5, ib6, ib7, ib8)
    return ikb


def get_keyboard_change_summa_crypto_ltc() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=3)
    ib1 = InlineKeyboardButton('100₽', callback_data='change_summ_crypto_ltc_100')
    ib2 = InlineKeyboardButton('200₽', callback_data='change_summ_crypto_ltc_200')
    ib3 = InlineKeyboardButton('300₽', callback_data='change_summ_crypto_ltc_300')
    ib4 = InlineKeyboardButton('400₽', callback_data='change_summ_crypto_ltc_400')
    ib5 = InlineKeyboardButton('500₽', callback_data='change_summ_crypto_ltc_500')
    ib6 = InlineKeyboardButton('600₽', callback_data='change_summ_crypto_ltc_600')
    ib7 = InlineKeyboardButton('Другая сумма', callback_data='change_summ_crypto_ltc_other')
    ib8 = InlineKeyboardButton('⬅️ Отмена', callback_data='back_to_profile')
    ikb.add(ib1, ib2, ib3, ib4, ib5, ib6, ib7, ib8)
    return ikb


def get_keyboard_change_summa_crypto_btc() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=3)
    ib1 = InlineKeyboardButton('100₽', callback_data='change_summ_crypto_btc_100')
    ib2 = InlineKeyboardButton('200₽', callback_data='change_summ_crypto_btc_200')
    ib3 = InlineKeyboardButton('300₽', callback_data='change_summ_crypto_btc_300')
    ib4 = InlineKeyboardButton('400₽', callback_data='change_summ_crypto_btc_400')
    ib5 = InlineKeyboardButton('500₽', callback_data='change_summ_crypto_btc_500')
    ib6 = InlineKeyboardButton('600₽', callback_data='change_summ_crypto_btc_600')
    ib7 = InlineKeyboardButton('Другая сумма', callback_data='change_summ_crypto_btc_other')
    ib8 = InlineKeyboardButton('⬅️ Отмена', callback_data='back_to_profile')
    ikb.add(ib1, ib2, ib3, ib4, ib5, ib6, ib7, ib8)
    return ikb


def get_keyboard_change_other_summa(change_payment, summa) -> InlineKeyboardMarkup:
    if change_payment == 0:
        data = f'change_summ_{summa}'
    elif change_payment == 1:
        data = f'change_summ_crypto_ltc_{summa}'
    elif change_payment == 2:
        data = f'change_summ_crypto_btc_{summa}'
    ikb = InlineKeyboardMarkup(row_width=1)
    ib1 = InlineKeyboardButton('✅ Продолжить', callback_data=data)
    ib2 = InlineKeyboardButton('⬅️ Отмена', callback_data="back_to_profile")
    ikb.add(ib1, ib2)
    return ikb


def get_keyboard_link_to_payment(url: str) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    ib1 = InlineKeyboardButton('💳 Перейти к оплате', url=url)
    ib2 = InlineKeyboardButton('⬅️ Отмена', callback_data='back_to_profile')
    ikb.add(ib1, ib2)
    return ikb


def get_keyboard_check_crypto_ltc() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    ib1 = InlineKeyboardButton('✅ Я оплатил(а)', callback_data=f'check_pay_crypto_ltc')
    ib2 = InlineKeyboardButton('ᅠ', callback_data='xxxxxxx')
    ib3 = InlineKeyboardButton('⬅️ Отмена', callback_data='back_to_profile')
    ikb.add(ib1, ib2, ib3)
    return ikb


def get_keyboard_check_crypto_btc() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    ib1 = InlineKeyboardButton('✅ Я оплатил(а)', callback_data=f'check_pay_crypto_btc')
    ib2 = InlineKeyboardButton('ᅠ', callback_data='xxxxxxx')
    ib3 = InlineKeyboardButton('⬅️ Отмена', callback_data='back_to_profile')
    ikb.add(ib1, ib2, ib3)
    return ikb


def get_keyboard_back_profile_general() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    ib1 = InlineKeyboardButton('⬅️ Главное меню', callback_data="back_to_profile")
    ikb.add(ib1)
    return ikb


def get_keyboard_succsess_pay() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    ib1 = InlineKeyboardButton('🧾 Получить чек', callback_data="get_me_receipt")
    ib2 = InlineKeyboardButton('⬅️ Главное меню', callback_data="back_to_profile")
    ikb.add(ib2)
    return ikb


def get_keyboard_admin() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    ib1 = InlineKeyboardButton('Сделать рассылку', callback_data='admin:message')
    ib2 = InlineKeyboardButton('Сделать рассылку с картинкой', callback_data='admin:message_image')
    ib3 = InlineKeyboardButton('Получить id video', callback_data='admin:video')
    ib4 = InlineKeyboardButton('Выйти', callback_data='admin:out')
    ikb.add(ib1, ib3, ib4)
    return ikb


def get_keyboard_admin_check_message() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=2)
    ib1 = InlineKeyboardButton('✅ Отправить', callback_data='admin:go_message')
    ib2 = InlineKeyboardButton('❌ Отмена', callback_data='admin:cancel_message')
    ikb.add(ib1, ib2)
    return ikb


def get_keyboard_up_balance_apshedule() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    ib1 = InlineKeyboardButton('💵 Пополнить баланс', callback_data='change_payment_method_rub')
    ikb.add(ib1)
    return ikb


def get_universe_menu_free_attemp_keyboard() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    ib1 = InlineKeyboardButton('➕ Подписаться', url="https://t.me/magneticpi")      # pay
    ib2 = InlineKeyboardButton('✅ Я Подписался', callback_data='check_member_chanel')      # pay
    ikb.add(ib1,ib2)
    return ikb


def get_keyboard_not_receipt() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    ib1 = InlineKeyboardButton('Не нужен чек', callback_data="skip_receipt")
    ikb.add(ib1)
    return ikb