from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from src.settings import get_bot_settings
from src.utils import get_keyboard


async def request_command(message: Message, bot: AsyncTeleBot):
    """Request command handler."""
    await bot.reply_to(message, get_bot_settings().request_str, reply_markup=get_keyboard())
