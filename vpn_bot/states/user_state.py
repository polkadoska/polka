from aiogram.dispatcher.filters.state import State, StatesGroup


class UserStateGroup(StatesGroup):
    change_country = State()
    change_device = State()
    change_tariff = State()
    change_protocol = State()
    input_summa = State()
    input_email = State()
    input_promocode = State()
    help = State()
    admin = State()
    admin_message = State()