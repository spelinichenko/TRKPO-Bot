from aiohttp import ClientSession
from pydantic import BaseModel
from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from src.enums import CafeType, Cuisine, District
from src.settings import get_bot_settings
from src.utils import create_str_response, get_keyboard


class RequestModel(BaseModel):
    district: District
    cuisine: Cuisine
    budget: int
    cafe_type: CafeType
    visitor_capacity: int


async def logic_message(message: Message, bot: AsyncTeleBot) -> None:
    """Logic message handler."""
    try:
        message_str: str = message.text
    except Exception:
        await bot.send_message(message.chat.id, "Сообщение должно быть в текстовом виде!", reply_markup=get_keyboard())
        return

    try:
        fields = RequestModel.model_fields.keys()
        fields_data = [line[2:].strip() for line in message_str.split("\n")]
        data = RequestModel(**dict(zip(fields, fields_data)))
    except Exception:
        await bot.send_message(
            message.chat.id, "Ошибка парсинга полей сообщения. Проверьте введенные данные!", reply_markup=get_keyboard()
        )
        return

    settings = get_bot_settings()
    async with ClientSession(settings.api_url) as session:
        async with session.post("/trkpo/request", json=data.model_dump()) as resp:
            if resp.content_type != "application/json":
                await bot.send_message(
                    message.chat.id,
                    "Произошла ошибка при обработке ответа API. Попробуйте заново!",
                    reply_markup=get_keyboard(),
                )
            result = await resp.json()

    if not isinstance(result, list):
        await bot.send_message(
            message.chat.id,
            "Произошла ошибка при обработке запроса. Попробуйте заново!",
            reply_markup=get_keyboard(),
        )

    if not result:
        await bot.send_message(
            message.chat.id,
            "К сожалению, бот не смог найти подходящие под ваш запрос помещения. "
            "Попробуйте изменить параметры запроса!",
            reply_markup=get_keyboard(),
        )

    await bot.send_message(
        message.chat.id, "\n\n".join([create_str_response(r) for r in result]), reply_markup=get_keyboard()
    )
