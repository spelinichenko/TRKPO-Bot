from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from src.utils import get_keyboard


async def request_command(message: Message, bot: AsyncTeleBot):
    """Request command handler."""
    await bot.reply_to(message, "Введите информацию в соответствии с шаблоном: ...", reply_markup=get_keyboard())
