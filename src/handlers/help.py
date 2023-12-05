from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from src.settings import get_bot_settings
from src.utils import get_keyboard


async def help_command(message: Message, bot: AsyncTeleBot):
    """Help command handler."""
    await bot.send_message(message.chat.id, get_bot_settings().help_str, reply_markup=get_keyboard())
