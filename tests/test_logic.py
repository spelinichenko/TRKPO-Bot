import json
from itertools import product
from unittest.mock import AsyncMock, MagicMock

import pytest
from telebot import TeleBot, apihelper
from telebot.types import CallbackQuery, Message
from telebot.util import CustomRequestResponse

from src.enums import CafeType, Cuisine, District
from src.handlers.logic import RequestModel, check_response, logic_message, process_request
from src.handlers.request import callback_handler, request_message_handler
from src.settings import get_bot_settings
from src.utils import get_keyboard


def custom_sender_logic(method, url, **kwargs):
    print("custom_sender. method: {}, url: {}, params: {}".format(method, url, kwargs.get("params")))
    result = CustomRequestResponse(
        '{"ok":true,"result":{"message_id": 1, "date": 1, "chat": {"id": 1, "type": "private"}}}'
    )
    return result


class MockChat:
    id = 15


def generate_test_cases_positive():
    test_cases = []

    budgets = [100_000, 1_000_000]
    visitor_capacity = [5, 100]

    combinations = product(District, Cuisine, budgets, CafeType, visitor_capacity)

    for combo in combinations:
        district, cuisine, budget, cafe_type, vis_cap = combo
        test_case_str = f"1. {district.value}\n2. {cuisine.value}\n3. {budget}\n4. {cafe_type.value}\n5. {vis_cap}"
        test_case_dict = {
            "district": district,
            "cuisine": cuisine,
            "budget": budget,
            "cafe_type": cafe_type,
            "visitor_capacity": vis_cap,
        }
        test_cases.append((test_case_str, test_case_dict))

    return test_cases


def generate_test_cases_negative():
    test_cases = []

    budgets = ["100_000", "123"]
    visitor_capacity = ["5", "dfksf"]

    combinations = product(District, Cuisine, budgets, CafeType, visitor_capacity)

    for combo in combinations:
        district, cuisine, budget, cafe_type, vis_cap = combo
        test_case_str = (
            f"1. {district.value + '1'}\n2. {cuisine.value}\n3. {budget}\n4. {cafe_type.value}\n5. {vis_cap}"
        )
        test_case_dict = {
            "district": district,
            "cuisine": cuisine,
            "budget": budget + "hhh",
            "cafe_type": cafe_type,
            "visitor_capacity": "-200",
        }
        test_cases.append((test_case_str, test_case_dict))

    return test_cases


@pytest.mark.parametrize("test_input, expected", generate_test_cases_positive())
async def test_logic_message(test_input, expected):
    message = Message(
        message_id=0, from_user=0, date="", chat=MockChat(), content_type="text", options=[], json_string=""
    )
    message.text = test_input

    apihelper.CUSTOM_REQUEST_SENDER = custom_sender_logic
    tb = TeleBot("test")

    with pytest.raises(Exception):
        await logic_message(message, tb)


async def test_logic_called():
    message = Message(
        message_id=0, from_user=0, date="", chat=MockChat(), content_type="text", options=[], json_string=""
    )
    message.text = "1. 100000\n2. 30\n3. central\n4. russia\n5. cafe"
    apihelper.CUSTOM_REQUEST_SENDER = custom_sender_logic

    sample_mock = AsyncMock()
    await logic_message(message, sample_mock)
    sample_mock.send_message.assert_awaited()


@pytest.mark.parametrize("test_str, test_dict", generate_test_cases_positive())
def test_request_model_positive(test_str, test_dict):
    assert RequestModel.model_validate(test_dict)


@pytest.mark.parametrize("test_str, test_dict", generate_test_cases_negative())
def test_request_model_negative(test_str, test_dict):
    with pytest.raises(Exception):
        RequestModel.model_validate(test_dict)


async def test_request_message_handler():
    apihelper.CUSTOM_REQUEST_SENDER = custom_sender_logic
    tb = TeleBot("test")
    with pytest.raises(Exception):
        await request_message_handler(123, tb)


@pytest.mark.parametrize("field", ["cuisine_russia", "type_cafe", "district_nevskiy"])
async def test_callback_handler(field):
    apihelper.CUSTOM_REQUEST_SENDER = custom_sender_logic
    tb = TeleBot("test")
    with pytest.raises(Exception):
        await callback_handler(
            CallbackQuery(
                id=123,
                from_user=123,
                data=field,
                chat_instance=123,
                json_string=123,
            )
        )


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
