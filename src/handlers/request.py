from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message, CallbackQuery

from src.utils import markup_inline_district, markup_inline_cuisine, \
    markup_inline_cafe_type

from src.settings import bot, results


async def request_message_handler(message: Message, bot: AsyncTeleBot):
    await bot.reply_to(message, "Выберите район",
                       reply_markup=markup_inline_district())


@bot.callback_query_handler(func=lambda callback: True)
async def callback_handler(call: CallbackQuery):
    choice = call.data

    if choice.startswith("district_"):
        results["district"] = choice.removeprefix("district_")

        await bot.send_message(chat_id=call.message.chat.id,
                               text='Вы выбрали "' + choice + '" район\n\nВыберите тип кухни',
                               reply_markup=markup_inline_cuisine())

    elif choice.startswith("cuisine_"):

        results["cuisine"] = choice.removeprefix("cuisine_")

        await bot.send_message(chat_id=call.message.chat.id,
                               text='Вы выбрали "' + choice + '" кухню\n\nВыберите тип заведения',
                               reply_markup=markup_inline_cafe_type())

    elif choice.startswith("type_"):
        results["cafe_type"] = choice.removeprefix("type_")

        await bot.send_message(chat_id=call.message.chat.id,
                               text='Введите в виде числа:\n1. Бюджет на аренду помещения (месяц, руб) (400000)\n'
                                    '2. Вместимость (желаемое количество человек) (10)',
                               reply_markup=None)
