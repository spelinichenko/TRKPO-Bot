import json
from unittest.mock import AsyncMock, MagicMock

import pytest

from src.enums import District, Cuisine, CafeType
from src.handlers.logic import check_response, RequestModel, process_request
from src.settings import get_bot_settings
from src.utils import get_keyboard


class MockResponse:
    def __init__(self, text, status):
        self._text = text
        self.status = status
        self.content_type = "application/json"

    async def text(self):
        return self._text

    async def __aexit__(self, exc_type, exc, tb):
        pass

    async def __aenter__(self):
        return self

    async def json(self):
        return json.loads(self._text)


@pytest.mark.integration
async def test_api_positive(mocker):
    bot_mock = AsyncMock()
    message_mock = MagicMock()
    message_mock.chat.id = "12345"

    result = {
        "street": "ул. Пушкина",
        "accuracy_address": "ул. Пушкина, дом Колотушкина",
        "room_area": 228,
        "room_price": 10000,
        "working_hours": "00:00-23:00",
        "delivery": True,
        "link": "test.com",
    }
    await check_response(result, bot_mock, message_mock)


@pytest.mark.integration
@pytest.mark.parametrize(
    "response,message",
    [
        ({}, "Произошла ошибка при обработке запроса. Попробуйте заново!"),
        (
            [],
            "К сожалению, бот не смог найти подходящие под ваш запрос помещения. "
            "Попробуйте изменить параметры запроса!",
        ),
    ],
)
async def test_api_negative(response, message, mocker):
    settings = get_bot_settings()
    data = RequestModel(
        district=District.central, cuisine=Cuisine.japan, cafe_type=CafeType.cafe, budget=100000, visitor_capacity=15
    )
    bot_mock = AsyncMock()
    message_mock = MagicMock()
    message_mock.chat.id = "12345"

    resp = MockResponse(json.dumps(response), 200)
    mocker.patch("aiohttp.ClientSession.post", return_value=resp)

    result = await process_request(settings, data, bot_mock, message_mock)
    await check_response(result, bot_mock, message_mock)

    bot_mock.send_message.assert_awaited_with(message_mock.chat.id, message, reply_markup=get_keyboard())
