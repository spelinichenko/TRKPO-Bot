import pytest
from telebot import TeleBot, apihelper
from telebot.util import CustomRequestResponse

from src.handlers.help import help_command
from src.handlers.start import start_command
from src.settings import get_bot_settings
from src.utils import HELP_STR, INFO_STR, get_keyboard
from unittest.mock import AsyncMock, patch, Mock
from telebot.types import Message

async def test_help_command():
    message = Mock()
    message.chat.id = 123456789  # Пример ID чата

    # Создаем заглушку для объекта бота
    bot = AsyncMock()

    # Мокируем get_bot_settings() и get_keyboard(), чтобы они возвращали какие-то значения
    with patch('src.settings.get_bot_settings') as mock_get_bot_settings, \
            patch('src.utils.get_keyboard') as mock_get_keyboard:
        mock_get_bot_settings.return_value.help_str = HELP_STR
        mock_get_keyboard.return_value = get_keyboard()
        # Вызываем тестируемую функцию
        await start_command(message, bot)

        # Проверяем, что функция send_message была вызвана с ожидаемыми параметрами
        bot.send_message.assert_called_once_with(123456789,
                                                 INFO_STR,
                                                 reply_markup=get_keyboard())
