from functools import lru_cache
from telebot import types


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

REQUEST_STR = """Формат входных данных:
1. Район (admiralteysky, vasileostrovsky, vyborg, kalininsky, kirovsky, \
kolpinsky, krasnogvardeisky, krasnoselsky, kurortny, moscow, nevsky, \
petrogradsky, petrodvortsovy, primorsky, pushkinsky, frunzensky, central)
2. Тип кухни (russia, china, japan, georgia, italy, korea, mexico, uzbekistan)
3. Бюджет на аренду помещения (месяц, руб) (400000)
4. Тип заведения (restaurant, cafe, canteen) (cafe)
5. Вместимость (желаемое количество человек) (10)
"""


@lru_cache
def get_keyboard() -> types.ReplyKeyboardMarkup:
    help_btn = types.InlineKeyboardButton("/help")
    request_btn = types.InlineKeyboardButton("/request")
    keyboard = types.ReplyKeyboardMarkup(True)
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
