import os
from functools import lru_cache

from pydantic_settings import BaseSettings

from src.utils import INFO_STR, HELP_STR, REQUEST_STR


class BotSettings(BaseSettings):
    token: str = os.environ.get(
        "bot_token", "6984965949:AAEaVsTWvmDM-Ch9yWRP4wJ7jALWMH7GJg0"
    )  # TODO: move token to safer place

    api_url: str = os.environ.get("api_url", "http://localhost:8000")

    info_str: str = INFO_STR

    help_str: str = HELP_STR

    request_str: str = REQUEST_STR


@lru_cache
def get_bot_settings():
    return BotSettings()
