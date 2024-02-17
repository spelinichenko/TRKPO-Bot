import os
from functools import lru_cache
from typing import Dict

from pydantic_settings import BaseSettings
from telebot.async_telebot import AsyncTeleBot

from src.utils import INFO_STR, HELP_STR


class BotSettings(BaseSettings):
    token: str = os.environ.get(
        "bot_token", "6984965949:AAEaVsTWvmDM-Ch9yWRP4wJ7jALWMH7GJg0"
    )  # TODO: move token to safer place

    api_url: str = os.environ.get("api_url", "http://localhost:8000")

    info_str: str = INFO_STR

    help_str: str = HELP_STR


@lru_cache
def get_bot_settings():
    return BotSettings()


settings = get_bot_settings()
bot = AsyncTeleBot(settings.token)
results: Dict = {}
