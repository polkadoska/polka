from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


def get_keyboard_test() -> ReplyKeyboardMarkup:
    rk = ReplyKeyboardMarkup(resize_keyboard=True)
    b1 = KeyboardButton('test')
    rk.add(b1)
    return rk


def delete_keyboard() -> ReplyKeyboardRemove:
    return ReplyKeyboardRemove()