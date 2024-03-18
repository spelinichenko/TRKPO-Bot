import pytest

from src.handlers.logic import parse_request
from unittest.mock import AsyncMock, MagicMock
from src.settings import results
from src.utils import get_keyboard


@pytest.mark.integration
async def test_request_command_positive():
    bot_mock = AsyncMock()
    message_mock = MagicMock()
    message_mock.chat.id = "12345"

    results['district'] = 'vasileostrovsky'
    results['cuisine'] = 'china'
    results['cafe_type'] = 'canteen'
    message = "1. 123\n2. 123"

    message_mock.content_type = "text"
    message_mock.text = message

    response = await parse_request(message_mock, bot_mock)
    print('response = ', response)
    bot_mock.send_message.assert_called_with(
        message_mock.chat.id, "Ваш запрос:\n" + results.__str__())


@pytest.mark.integration
async def test_request_command_negative(clear_results):
    bot_mock = AsyncMock()
    message_mock = MagicMock()
    message_mock.chat.id = "12345"

    results['district'] = 'vasileostrovsky'
    results['cuisine'] = 'china'
    message = '1. 123\n2. 123'

    message_mock.content_type = "text"
    message_mock.text = message

    response = await parse_request(message_mock, bot_mock)
    print('response = ', response)
    bot_mock.send_message.assert_called_with(message_mock.chat.id, "Ошибка парсинга полей сообщения. Проверьте введенные данные!", reply_markup=get_keyboard())


@pytest.mark.integration
async def test_request_command_negative_photo(clear_results):
    bot_mock = AsyncMock()
    message_mock = MagicMock()
    message_mock.chat.id = "12345"
    message_mock.content_type = "document"

    with open("cloud.jpg", "rb") as photo:
        message_mock.text = photo

    response = await parse_request(message_mock, bot_mock)

    bot_mock.send_message.assert_called_with(message_mock.chat.id, "Сообщение должно быть в текстовом виде!", reply_markup=get_keyboard())
