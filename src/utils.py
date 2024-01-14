from functools import lru_cache
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
# from telebot import types

INFO_STR = """BizSpot Finder — ваш персональный помощник в открытии успешного бизнеса в общепите.

Этот бот предоставляет вам
информацию и аналитику для выбора наилучшего места
для вашего будущего предприятия.

Данный бот был создан в рамках курса ТРКПО
 и не является коммерческим продуктом.

Стек технологий:
 - Python 3.10+ используемый язык программирования.
 - FastAPI фреймворк для создания API
 - aiohttp библиотека асинхронных запросов
 - telebot библиотека для создания бота на python для Telegram.
 - OSMPythonTools  библиотека для доступа к базе OSM
 - Prometheus система мониторинга
 - Grafana система визуализации метрик

Разработчики:
- Самойленко Константин
- Рулев Григорий
- Цапов Никита
- Пелиниченко Степан

Год создания - 2023
"""

HELP_STR = """Доступные функции:
1) /start - краткая информация при инициализации бота
2) /help - информация по пользованию ботом
3) /request - отправить в обработку запрос в обработку

Формат входных данных:
1. Район
2. Тип кухни
3. Бюджет на аренду помещения (месяц, руб)
4. Тип заведения
5. Вместимость (желаемое количество человек)

Формат выходных данных:
1. Улица (по расположению соседних заведений)
2. Точный адрес помещения (по доступным объявлениям на Циан)
3. Площадь помещения (м2) (по доступным объявлениям на Циан)
4. Цена за помещение (руб/мес) (по доступным объявлениям на Циан)
5. Выгодное время работы (временной промежуток) (по времени раброты соседних заведений)
6. Возможность доставки (по возможности доставки соседних заведений)
"""


def markup_inline_district() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("Адмиралтейский", callback_data="district_admiralteysky"),
        InlineKeyboardButton("Василеостровский", callback_data="district_vasileostrovsky"),
        InlineKeyboardButton("Выборг", callback_data="district_vyborg"),
        InlineKeyboardButton("Калининский", callback_data="district_kalininsky"),
        InlineKeyboardButton("Кировский", callback_data="district_kirovsky"),
        InlineKeyboardButton("Колпинский", callback_data="district_kolpinsky"),
        InlineKeyboardButton("Красногвардейский", callback_data="district_krasnogvardeisky"),
        InlineKeyboardButton("Красносельский", callback_data="district_krasnoselsky"),
        InlineKeyboardButton("Крондштат", callback_data="district_kronstadt"),
        InlineKeyboardButton("Невский", callback_data="district_nevsky"),
        InlineKeyboardButton("Московский", callback_data="district_moscow"),
        InlineKeyboardButton("Петроградский", callback_data="district_petrogradsky"),
        InlineKeyboardButton("Петродворцовый", callback_data="district_petrodvortsovy"),
        InlineKeyboardButton("Приморский", callback_data="district_primorsky"),
        InlineKeyboardButton("Пушкинский", callback_data="district_pushkinsky"),
        InlineKeyboardButton("Фрунзенский", callback_data="district_frunzensky"),
        InlineKeyboardButton("Центральный", callback_data="district_central"),
    )
    return markup


def markup_inline_cuisine() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("Русская", callback_data="cuisine_russia"),
        InlineKeyboardButton("Китайская", callback_data="cuisine_china"),
        InlineKeyboardButton("Японская", callback_data="cuisine_japan"),
        InlineKeyboardButton("Грузинская", callback_data="cuisine_georgia"),
        InlineKeyboardButton("Итальянская", callback_data="cuisine_italy"),
        InlineKeyboardButton("Корейская", callback_data="cuisine_korea"),
        InlineKeyboardButton("Мексиканская", callback_data="cuisine_mexico"),
        InlineKeyboardButton("Узбекская", callback_data="cuisine_uzbekistan")
    )
    return markup


def markup_inline_cafe_type() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("Ресторан", callback_data="type_restaurant"),
        InlineKeyboardButton("Кафе", callback_data="type_cafe"),
        InlineKeyboardButton("Столовая", callback_data="type_canteen")
    )
    return markup

@lru_cache
def get_keyboard() -> ReplyKeyboardMarkup:
    help_btn = InlineKeyboardButton("/help")
    request_btn = InlineKeyboardButton("/request")
    keyboard = ReplyKeyboardMarkup(True)
    keyboard.row(help_btn, request_btn)
    return keyboard


def create_str_response(data: dict) -> str:
    return f"""
1. Ссылка на объявление: {data.get("link")}
2. Улица: {data.get("street")}
3. Точный адрес помещения: {data.get("accuracy_address")}
4. Площадь помещения (м2): {data.get("room_area")}
5. Цена за помещение (руб/мес): {data.get("room_price")}
6. Выгодное время работы: {data.get("working_hours")}
7. Возможность доставки: {"Рекомендуется" if data.get("delivery") else "Не влияет"}
"""
