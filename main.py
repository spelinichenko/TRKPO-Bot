import asyncio
from src.handlers.start import start_command
from src.handlers.help import help_command
from src.handlers.request import request_message_handler
from src.handlers.logic import logic_message
from src.settings import bot

bot.register_message_handler(start_command, commands=["start"], pass_bot=True)
bot.register_message_handler(help_command, commands=["help"], pass_bot=True)
bot.register_message_handler(request_message_handler, commands=["request"],
                             pass_bot=True)
bot.register_message_handler(logic_message, pass_bot=True)

asyncio.run(bot.polling())
