from functools import lru_cache
from telebot import types


@lru_cache
def get_keyboard() -> types.ReplyKeyboardMarkup:
    help_btn = types.InlineKeyboardButton("/help")
    request_btn = types.InlineKeyboardButton("/request")
    keyboard = types.ReplyKeyboardMarkup(True)
    keyboard.row(help_btn, request_btn)
    return keyboard
