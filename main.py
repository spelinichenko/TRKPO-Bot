import asyncio

from telebot.async_telebot import AsyncTeleBot

from src.handlers.start import start_command
from src.handlers.help import help_command
from src.handlers.request import request_command
from src.handlers.logic import logic_message
from src.settings import get_bot_settings

settings = get_bot_settings()

bot = AsyncTeleBot(settings.token)
bot.register_message_handler(start_command, commands=["start"], pass_bot=True)
bot.register_message_handler(help_command, commands=["help"], pass_bot=True)
bot.register_message_handler(request_command, commands=["request"], pass_bot=True)
bot.register_message_handler(logic_message, pass_bot=True)

asyncio.run(bot.polling())
