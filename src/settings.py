import os
from functools import lru_cache

from pydantic_settings import BaseSettings


class BotSettings(BaseSettings):
    token: str = os.environ.get(
        "bot_token", "6984965949:AAEaVsTWvmDM-Ch9yWRP4wJ7jALWMH7GJg0"
    )  # TODO: move token to safer place

    api_url: str = os.environ.get("api_url", "http://localhost:8000")

    info: str = """Добро пожаловать в бот
        для работы с сервисом анализа подходящего места
        для открытия точки бизнеса, связанной с общепитом
        """

    help: str = """Доступные функции:
1) /start - краткая информация при инициализации бота
2) /help - информация по пользованию ботом
3) /request - отправить в обработку запрос в обработку

Формат входных данных: TODO
Формат выходных данных: TODO
"""


@lru_cache
def get_bot_settings():
    return BotSettings()
