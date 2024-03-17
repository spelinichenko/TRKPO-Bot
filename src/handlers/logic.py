import re
from typing import Any

from aiohttp import ClientSession
from pydantic import BaseModel
from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from src.enums import CafeType, Cuisine, District
from src.settings import BotSettings, bot, results, get_bot_settings
from src.utils import create_str_response, get_keyboard


class RequestModel(BaseModel):
    district: District
    cuisine: Cuisine
    cafe_type: CafeType
    budget: int
    visitor_capacity: int


async def logic_message(message: Message, bot: AsyncTeleBot) -> None:
    """Logic message handler."""
    if message.content_type != "text":
        await bot.send_message(message.chat.id, "Сообщение должно быть в текстовом виде!", reply_markup=get_keyboard())
        return
    else:
        message_str: str = message.text
    try:
        lines = message_str.split("\n")
        parts = [re.sub(r"^\d+\.\s*", "", s) for s in lines]
        results["budget"] = int(parts[0])
        results["visitor_capacity"] = int(parts[1])
        await bot.send_message(message.chat.id, "Ваш запрос:\n" + results.__str__())
        fields = RequestModel.model_fields.keys()
        fields_data = [value for _, value in results.items()]
        data = RequestModel(**dict(zip(fields, fields_data)))

    except Exception:
        await bot.send_message(
            message.chat.id, "Ошибка парсинга полей сообщения. Проверьте введенные данные!", reply_markup=get_keyboard()
        )
        return

    settings = get_bot_settings()

    result = await process_request(settings, data, bot, message)
    await check_response(result, bot, message)


async def process_request(settings: BotSettings, data: RequestModel, bot: AsyncTeleBot, message: Message) -> Any:
    async with ClientSession(settings.api_url) as session:
        async with session.post("/trkpo/request", json=data.model_dump()) as resp:
            if resp.content_type != "application/json":
                await bot.send_message(
                    message.chat.id,
                    "Произошла ошибка при обработке ответа API. Попробуйте заново!",
                    reply_markup=get_keyboard(),
                )
            return await resp.json()


async def check_response(result: Any, bot: AsyncTeleBot, message: Message) -> Any:
    if not isinstance(result, list):
        await bot.send_message(
            message.chat.id,
            "Произошла ошибка при обработке запроса. Попробуйте заново!",
            reply_markup=get_keyboard(),
        )
        return

    if not result:
        await bot.send_message(
            message.chat.id,
            "К сожалению, бот не смог найти подходящие под ваш запрос помещения. "
            "Попробуйте изменить параметры запроса!",
            reply_markup=get_keyboard(),
        )
        return

    await bot.send_message(
        message.chat.id, "\n\n".join([create_str_response(r) for r in result]), reply_markup=get_keyboard()
    )


async def check_request(result: Any, bot: AsyncTeleBot, message: Message) -> Any:
    if not isinstance(result, list):
        await bot.send_message(
            message.chat.id,
            "Сообщение должно быть в текстовом виде!",
            reply_markup=get_keyboard(),
        )
        return

    if not result:
        await bot.send_message(
            message.chat.id,
            "Ошибка парсинга полей сообщения. Проверьте введенные данные!",
            reply_markup=get_keyboard(),
        )
        return

    await bot.send_message(message.chat.id, "Ваш запрос:\n" + results.__str__())
