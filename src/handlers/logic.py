from aiohttp import ClientSession
from pydantic import BaseModel
from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from src.enums import CafeType, Cuisine, District
from src.settings import get_bot_settings
from src.utils import get_keyboard


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
            result = await resp.json()

    await bot.send_message(message.chat.id, result)
