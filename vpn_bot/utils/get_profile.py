import logging
from data.config import dict_server, dict_tariff


async def get_profile_data(user_data) -> str:
    try:
        days = user_data['balance'] // (user_data['count_configs'] * user_data['sum_tariff'])
    except ZeroDivisionError:
        days = 'Бесконечно'
    text_profile = f"<b>Ваш личный кабинет</b>\nРады выдеть вас снова!\n\n<b>Ваш id:</b> <code><b>{user_data['user_id']}</b></code> \n(нажми чтобы скопировать)\n<b>Баланс:</b> <b>{user_data['balance']}</b> руб.\n<b>Тариф:</b> <b>{user_data['sum_tariff']}</b> руб/сутки\nХватит на <b>{days}</b> дня(ей) \n\n<b>Описание кнопок:</b> \n\n💻<b>Мои устройства:</b> Тут вы можете создавать, просматривать и удалять ваши подключения/устройства. \n\n💳<b>Пополнить баланс:</b> Пополнение баланса является однократной операцией <b>(не подписка)</b>. Мы не имеем доступа к вашим личным и платежным данным.\n\n🆘<b>Помощь:</b> Написать обращение в администрацию сервиса."
    if user_data['friend']:
        text_profile = f"<b>Ваш личный кабинет</b>\nРады видеть вас снова!\n\n<b>Ваш id:</b> <code><b>{user_data['user_id']}</b></code> \n(нажми чтобы скопировать)\n<b>Ваш статус: Free </b>\n\n<b>Описание кнопок:</b> \n\n💻<b>Мои устройства:</b> Тут вы можете создавать, просматривать и удалять ваши подключения/устройства. \n\n💳<b>Пополнить баланс:</b> Пополнение баланса является однократной операцией <b>(не подписка)</b>. Мы не имеем доступа к вашим личным и платежным данным.\n\n🆘<b>Помощь:</b> Написать обращение в администрацию сервиса."
    return text_profile

    

async def get_profile_user_device(device_info) -> str:
    try:
        text_device = f"Информация о вашем конфиге\n\nИмя конфига: <b>{device_info['config_name']}</b>\nТариф: <b>{dict_tariff[device_info['tariff']]}</b>\nСтрана: <b>{dict_server[device_info['number_server']]['country']}</b>"
    except Exception as e:
        text_device = f"Информация о вашем конфиге\n\nИмя конфига: <b>{device_info['config_name']}</b>\nТариф: <b>STANDARD</b>\nСтрана: <b>{dict_server[device_info['number_server']]['country']}</b>"
    return text_device
