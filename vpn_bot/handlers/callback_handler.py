import datetime
import logging
import aiofiles.os
from aiogram.dispatcher.filters import Text
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageNotModified
from contextlib import suppress

from loader import dp, bot
from keyboards import inline, reply
from states import *
from utils import API, get_profile
from data import config
from db import mysql
from utils.API_X import add_user_x, delete_user_x


async def edit_message(message: types.Message, new_text: str, reply_markup=None):
    with suppress(MessageNotModified):
        await message.edit_text(new_text, reply_markup=reply_markup)


@dp.callback_query_handler(Text(startswith='change_device_'), state=user_state.UserStateGroup.change_device)
async def callback_change_device(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer(None)
    user_id = str(callback.from_user.id)
    type_device = int(callback.data[14:])
    await edit_message(callback.message, 
                       callback.message.text, 
                       inline.get_keyboard_change_device(type_device))
    await state.update_data(type_device=type_device)
    new_text = "<b>Выберете тариф</b>\n\n<b>Тариф</b> <b>STANDARD:</b>  весь трафик шифруется \n\nНа данный момент у нас всего один тариф. \n\n Для продолжения нажмите на тариф⬇️"
    await callback.message.answer(new_text, reply_markup=inline.get_keyboard_change_tariff())
    return await state.set_state(user_state.UserStateGroup.change_tariff.state)


@dp.callback_query_handler(Text(startswith="change_tariff_"), state=user_state.UserStateGroup.change_tariff)
async def callback_change_tariff(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer(None)
    user_id = str(callback.from_user.id)
    tariff = int(callback.data[14:])
    await edit_message(callback.message, callback.message.text, inline.get_keyboard_change_tariff(tariff))
    await state.update_data(tariff=tariff)
    new_text = "<b>Выберете протокол соединения:</b>"
    await callback.message.answer(new_text, reply_markup=inline.get_keyboard_change_protocol())
    return await state.set_state(user_state.UserStateGroup.change_protocol.state)
 
@dp.callback_query_handler(Text(startswith='change_protocol_'), state=user_state.UserStateGroup.change_protocol)
async def callback_change_protocol(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer(None)
    protocol = int(callback.data[16:])
    await edit_message(
        callback.message, 
        callback.message.text, 
        inline.get_keyboard_change_protocol(protocol)
        )
    await state.update_data(protocol=protocol)
    new_text = "<b>Выберете страну для Вашего нового устройства:</b>"
    await callback.message.answer(
        new_text, 
        reply_markup=inline.get_keyboard_change_country()
        )
    print(await state.get_data())
    return await state.set_state(user_state.UserStateGroup.change_country.state)


@dp.callback_query_handler(Text(startswith='change_country_'), state=user_state.UserStateGroup.change_country)
async def callback_change_coutry(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer(None)
    user_id = str(callback.from_user.id)
    coutry_server = int(callback.data[15:])
    await edit_message(
        callback.message, 
        callback.message.text, 
        inline.get_keyboard_change_country(coutry_server)
        )
    awaiting_message = await callback.message.answer('Подождите несколько секунд ваша конфигурация создается ...')
    await state.update_data(number_server=coutry_server)
    user_data = await state.get_data()
    print(user_data)
    if user_data['protocol'] == 1:
        if user_data['type_device'] == 1:
            try:
                await callback.message.answer_video(config.VIDEO_IOS, caption="<b>Видеоинструкция по установке</b>")
            except Exception as e:
                logging.exception(e)
        elif user_data['type_device'] == 2:
            try:
                await callback.message.answer_video(config.VIDEO_ANDROID, caption="<b>Видеоинструкция по установке</b>")
            except Exception as e:
                logging.exception(e)
        elif user_data['type_device'] == 3:
            try:
                await callback.message.answer_video(config.VIDEO_WINDOWS_WG, caption="<b>Видеоинструкция по установке</b>")
            except Exception as e:
                logging.exception(e)
        elif user_data['type_device'] == 4:
            try:
                await callback.message.answer_video(config.VIDEO_MAC_WG, caption="<b>Видеоинструкция по установке</b>")
            except Exception as e:
                logging.exception(e)        

        new_name = await API.check_count_peer_with_user_id(user_id)
        return_add = await API.add_peer(config.dict_server[user_data['number_server']]['url'], config.dict_server[user_data['number_server']]['password'], new_name)
        if not 'error' in return_add:
            date_end = datetime.date.today() + datetime.timedelta(3)
            user_info_server = await API.get_user_info_from_server(config.dict_server[user_data['number_server']]['url'], config.dict_server[user_data['number_server']]['password'], return_add['name'])
            await mysql.add_config(user_id, return_add['name'], user_data['number_server'], user_data['tariff'], date_end, user_info_server['id'], user_data['type_device'], user_data['protocol'])
            return_add['end_point'] = config.dict_server[user_data['number_server']]['end_point']
            path_qr_code, path_conf_file = await API.create_conf_file(return_add, user_data['number_server'], config.dict_server[user_data['number_server']]['public_key'], user_data['tariff'])
            await callback.message.answer_document(document=open(path_conf_file, "rb"), caption=f"""1️⃣ пусто""", reply_markup=inline.get_keyboard_profile())
            await state.finish()
        else:
            await callback.message.answer('Произошла ошибка, попробуйте еще раз /start или обратитесь за помощью к администрации')
            await state.finish()

    elif user_data['protocol'] in [2, 3, 4, 5]:
        date_end = datetime.date.today() + datetime.timedelta(3)
        new_name = await API.check_count_peer_with_user_id(user_id)
        resuld_add = await add_user_x(
            new_name, 
            user_data['protocol'], 
            number_server=user_data['number_server']
            )
        if resuld_add:
            if user_data['type_device'] == 1:
                try:
                    await callback.message.answer_video(config.VIDEO_IOS_X, caption="<b>Видеоинструкция по установке</b>")
                except Exception as e:
                    logging.exception(e)
            elif user_data['type_device'] == 2:
                try:
                    await callback.message.answer_video(config.VIDEO_ANDROID_X, caption="<b>Видеоинструкция по установке</b>")
                except Exception as e:
                    logging.exception(e)
            elif user_data['type_device'] == 3:
                try:
                    await callback.message.answer_video(config.VIDEO_WINDOWS_X, caption="<b>Видеоинструкция по установке</b>")
                except Exception as e:
                    logging.exception(e)
            elif user_data['type_device'] == 4:
                try:
                    await callback.message.answer_video(config.VIDEO_MAC_X, caption="<b>Видеоинструкция по установке</b>")
                except Exception as e:                
                    logging.exception(e)                    
            await mysql.add_config(str(callback.from_user.id),
                                new_name,
                                user_data['number_server'],
                                user_data['tariff'],
                                date_end,
                                new_name,
                                user_data['type_device'],
                                user_data['protocol'])
            await callback.message.answer(f"""1️⃣ <b>Скачайте приложение</b>

<b>IOS:</b> <a href='https://apps.apple.com/ru/app/v2box-v2ray-client/id6446814690'>Скачать</a>

<b>Android:</b> <a href='https://play.google.com/store/apps/details?id=com.v2ray.ang'>Скачать</a>

<b>Windows:</b> <a href='https://getoutline.org/ru/get-started/#step-3'>Скачать</a>

<b>MacOS:</b> <a href='https://apps.apple.com/us/app/outline-app/id1356178125'>Скачать</a>

                                        
2️⃣ <b>Скопируйте конфигурацию и добавте ее в приложение.</b>

<b>Вам нужно просто скопировать код ниже, вставить его в приложение и включить.</b>

<i>Нажмите, чтобы скопировтаь ⬇️</i>
<code>{resuld_add}</code>

""", reply_markup=inline.get_keyboard_profile(), disable_web_page_preview=True)
            await state.finish()
        else:
            await callback.message.answer('Произошла ошибка, повторите действие заново /start')
            await state.finish()


@dp.callback_query_handler(Text(startswith='get_profile'), state="*")
async def callback_get_profile(callback: types.CallbackQuery, state: FSMContext):
    try:
        await callback.answer(None)
    except Exception as e:
        logging.exception(f"Ошибка на ответ callback answer{e}")
    result = await mysql.get_user_info(str(callback.from_user.id))
    text_profile = await get_profile.get_profile_data(result)
    await callback.message.answer(text_profile, disable_web_page_preview=True, reply_markup=inline.get_keyboard_menu_profile())


@dp.callback_query_handler(Text(startswith='my_device'), state="*")
async def callback_my_device(callback: types.CallbackQuery, state: FSMContext):
    try:
        await callback.answer(None)
        user_device = await mysql.get_user_device(str(callback.from_user.id))
        await edit_message(callback.message, f"<b>Список ваших устройств</b>\n\nВ этом разделе вы можете управлять вашими конфигурационными файлами\n\nВы можете добавить устройство нажав кнопку <b>+Добавить Устройство</b>\n\n\Обращаем внимание что в данный момент повторно скачать конфиг Shadowsocks не получится, если вы его потеряли то просто удалите старый и создайте новый." , 
                           reply_markup=inline.get_keyboard_list_device(user_device))
    except Exception as e:
        logging.exception(f"Ошибка в кнопке Мои устройства: {e}")
        user_device = await mysql.get_user_device(str(callback.from_user.id))
        print(user_device)
        await callback.message.answer(f"<b>Список ваших устройств</b>\n\nВ этом разделе вы можете управлять вашими конфигурационными файлами\n\nВы можете добавить устройство нажав кнопку <b>+Добавить Устройство</b>\n\n\Обращаем внимание что в данный момент повторно скачать конфиг Shadowsocks не получится, если вы его потеряли то просто удалите старый и создайте новый.",
                                      reply_markup=inline.get_keyboard_list_device(user_device))


@dp.callback_query_handler(Text(equals='back_to_profile'), state="*")
async def callback_back_to_profile(callback: types.CallbackQuery, state: FSMContext):
    try:
        await callback.answer(None)
        user_info = await mysql.get_user_info(str(callback.from_user.id))
        text_profile = await get_profile.get_profile_data(user_info)
        await edit_message(
            callback.message, 
            text_profile, 
            reply_markup=inline.get_keyboard_menu_profile()
            )
        await state.finish()
    except Exception as e:
        await state.finish()
        user_info = await mysql.get_user_info(str(callback.from_user.id))
        text_profile = await get_profile.get_profile_data(user_info)
        await callback.message.answer(
            text_profile, 
            reply_markup=inline.get_keyboard_menu_profile()
            )


@dp.callback_query_handler(Text(startswith='but_back_to:'), state="*")
async def callback_but_back_to(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    if callback.data == 'but_back_to:change_device':
        return await state.set_state(user_state.UserStateGroup.change_device.state)
    elif callback.data == 'but_back_to:change_tariff':
        return await state.set_state(user_state.UserStateGroup.change_tariff.state)
    elif callback.data == 'but_back_to:change_country':
        return await state.set_state(user_state.UserStateGroup.change_country.state)
    elif callback.data == 'but_back_to:change_protocol':
        return await state.set_state(user_state.UserStateGroup.change_protocol.state)


@dp.callback_query_handler(Text(startswith='change_device_info_'), state="*")
async def callback_change_device_info(callback: types.CallbackQuery, state: FSMContext):
    try:
        await callback.answer(None)
        config_name = callback.data[19:]
        device_info = await mysql.get_user_change_device(config_name)
        try:
            text_device = await get_profile.get_profile_user_device(device_info)
            await edit_message(callback.message, 
                               text_device, 
                               reply_markup=inline.get_keyboard_controll_device(device_info['id_server']))
            # await state.update_data(device_info=dict(device_info))
        except Exception as e:
            logging.exception(f"Ошибка при выборе конкретного конфига пользователем. {config_name} {e}")
            text_device = await get_profile.get_profile_user_device(device_info)
            await callback.message.answer(text_device,
                                          reply_markup=inline.get_keyboard_controll_device(device_info['id_server']))
    except Exception as e:
        logging.exception(f"Главная ошибка при выборе конкретного конфига пользователем. {config_name} {e}")
        await callback.message.answer('Произошла ошибка. \n<b>Сообщите о ней администрации. Код: 002</b>')


@dp.callback_query_handler(Text(equals="add_device"), state="*")
async def callback_add_device(callback: types.CallbackQuery, state: FSMContext):
    try:
        user_info = await mysql.get_user_info(str(callback.from_user.id))
        if user_info['balance'] == 0:
            return await callback.answer(
                'Вам необходимо пополнить баланс на любую сумму, чтобы вновь создавать новые конфигурационные файлы', 
                show_alert=True)
        elif user_info['count_configs'] > 9:
            return await callback.answer(
                'Вы не можете создавать больше 10 конфигурационных файлов', 
                show_alert=True)
        new_text = "<b>Выберете тип вашего нового устройства</b>"
        await edit_message(
            callback.message, 
            new_text, 
            reply_markup=inline.get_keyboard_change_device()
            )
        return await state.set_state(user_state.UserStateGroup.change_device.state)
    except Exception as e:
        logging.exception(f"Ошибка при нажатии кнопки Добавить устройство {str(callback.from_user.id)} {e}")
        user_info = await mysql.get_user_info(str(callback.from_user.id))
        if user_info['balance'] == 0:
            return await callback.answer(
                'Вам необходимо пополнить баланс на любую сумму, чтобы вновь создавать новые конфигурационные файлы', 
                show_alert=True)
        elif user_info['count_configs'] > 9:
            return await callback.answer(
                'Вы не можете создавать больше 10 конфигурационных файлов', 
                show_alert=True)
        new_text = "<b>Выберете тип вашего нового устройства</b>"
        await callback.message.answer(
            new_text, 
            reply_markup=inline.get_keyboard_change_device())
        return await state.set_state(user_state.UserStateGroup.change_device.state)


@dp.callback_query_handler(Text(startswith="del_"), state="*")
async def callback_del_device(callback: types.CallbackQuery, state: FSMContext):
    id = callback.data[4:]
    device_info = await mysql.get_config_info(id)
    if len(device_info['id_server']) > 20:
        result = await API.delete_peer(
            config.dict_server[device_info['number_server']]['url'], 
            config.dict_server[device_info['number_server']]['password'], 
            id)
    else:
        await delete_user_x(
            device_info['config_name'], 
            device_info['number_server']
            )
        result = True
    if result:
        await mysql.delete_peer(device_info['config_name'])
        try:
            await aiofiles.os.remove(f"./conf_file/{device_info['number_server']}/{device_info['config_name']}.conf")
            await aiofiles.os.remove(f"./qr_code/{device_info['number_server']}/{device_info['config_name']}.png")
        except Exception as e:
            logging.exception(e)
        await callback.answer('Удалено')
        user_device = await mysql.get_user_device(str(callback.from_user.id))
        await edit_message(
            callback.message, 
            '📱 💻 🖥<b>Список ваших устройств</b><b>(Список ваших устройств)</b>\n\nВ этом разделе вы можете управлять вашими конфигурационными файлами\n\nВы можете добавить устройство нажав кнопку <b>+Добавить Устройство</b>\n\n\Обращаем внимание что в данный момент повторно скачать конфиг Shadowsocks не получится, если вы его потеряли то просто удалите старый и создайте новый.', 
            reply_markup=inline.get_keyboard_list_device(user_device))
    else:
        await callback.answer('Ошибка')


@dp.callback_query_handler(Text(startswith="conf_"), state="*")
async def callback_get_conf_file(callback: types.CallbackQuery, state: FSMContext):
    id = callback.data[5:]
    device_info = await mysql.get_config_info(id)
    if len(device_info['id_server']) > 20:
        try:
            await callback.message.answer_document(
                document=open(f"./conf_file/{device_info['number_server']}/{device_info['config_name']}.conf", "rb"), 
                reply_markup=inline.get_keyboard_hide_conf_file()
                )
            await callback.answer(None)
        except Exception as e:
            logging.error(f"Ошибка в кнопке показать конфиг {id} {e}")
            await callback.answer('Ошибка: код 003')
    else:
        await callback.answer('Скачать конфиг повторно пока не получится, мы работаем над этим.')


@dp.callback_query_handler(Text(equals="hide_config"), state="*")
async def callback_hide_conf_file(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer(None)
    await callback.message.delete()


@dp.callback_query_handler(Text(equals="referal_system"), state="*")
async def callback_referal_system(callback: types.CallbackQuery, state: FSMContext):
    user_id = str(callback.from_user.id)
    user_info = await mysql.get_user_info(user_id)
    count_referal = len(await mysql.get_my_referal(user_id))
    config_bot = await mysql.get_sum_tariff()
    referal_info, referal_url = await get_profile.get_referal_info(config.BOT_NAME,
                                                                    user_id,
                                                                    count_referal,
                                                                    user_info['referal_balance'],
                                                                    config_bot['referal_procent'])
    await edit_message(
        callback.message, 
        referal_info, 
        reply_markup=inline.get_keyboard_referal_system(referal_url))
    

@dp.callback_query_handler(Text(equals="out_money"), state="*")
async def callback_out_money(callback: types.CallbackQuery, state: FSMContext):
    user_id = str(callback.from_user.id)
    user_info = await mysql.get_user_info(user_id)
    if user_info['referal_balance'] < 100:
        return await callback.answer("Недостаточно", show_alert=True)
    try:
        await bot.send_message(chat_id=config.ADMINS_CHAT, 
                               text=f" <code>{user_id}</code> @{user_info['user_name']}\n1</b>: сумма {user_info['referal_balance']}")
        await edit_message(callback.message, "✅ <b>1",
                           reply_markup=inline.get_keyboard_back_profile_general())
    except Exception as e:
        await bot.send_message(chat_id=config.ADMINS_CHAT, 
                               text=f" <code>{user_id}</code> @{user_info['user_name']}\n <b>1</b>: сумма {user_info['referal_balance']}")
        await callback.message.answer("✅ .",
                                      reply_markup=inline.get_keyboard_back_profile_general())
    

@dp.callback_query_handler(Text(equals="help_system"), state="*")
async def callback_help_system(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer(None)
    text = "Напишите в чат свой вопрос максимально развернуто!\nМы обязательно ответим на него в ближайшее время!\n\nСпасибо что пользуетесь нашим сервисом "
    await edit_message(callback.message, new_text=text, reply_markup=inline.get_keyboard_back_profile_general())
    await state.set_state(user_state.UserStateGroup.help.state)


@dp.callback_query_handler(Text(equals="get_me_receipt"), state="*")
async def callback_get_me_receipt(callback: types.CallbackQuery, state: FSMContext):
    await edit_message(callback.message, "<b>Чек будет отправлен вам в телеграм бота в течении 24 часов.</b>\n\nСпасибо, что пользуетесь нашим сервисом")
    await bot.send_message(chat_id=config.ADMINS_CHAT, text=f"🧾 <b>{callback.from_user.id}</b> запрашивает чек.")
