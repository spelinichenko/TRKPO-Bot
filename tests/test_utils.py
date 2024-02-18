from typing import List
import pytest
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, \
    ReplyKeyboardMarkup

from src.utils import create_str_response, markup_inline_cafe_type, \
    markup_inline_cuisine, markup_inline_district


@pytest.fixture
def inline_keyboard_district():
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("Адмиралтейский",
                             callback_data="district_admiralteysky"),
        InlineKeyboardButton("Василеостровский",
                             callback_data="district_vasileostrovsky"),
        InlineKeyboardButton("Выборг", callback_data="district_vyborg"),
        InlineKeyboardButton("Калининский",
                             callback_data="district_kalininsky"),
        InlineKeyboardButton("Кировский", callback_data="district_kirovsky"),
        InlineKeyboardButton("Колпинский", callback_data="district_kolpinsky"),
        InlineKeyboardButton("Красногвардейский",
                             callback_data="district_krasnogvardeisky"),
        InlineKeyboardButton("Красносельский",
                             callback_data="district_krasnoselsky"),
        InlineKeyboardButton("Крондштат", callback_data="district_kronstadt"),
        InlineKeyboardButton("Невский", callback_data="district_nevsky"),
        InlineKeyboardButton("Московский", callback_data="district_moscow"),
        InlineKeyboardButton("Петроградский",
                             callback_data="district_petrogradsky"),
        InlineKeyboardButton("Петродворцовый",
                             callback_data="district_petrodvortsovy"),
        InlineKeyboardButton("Приморский", callback_data="district_primorsky"),
        InlineKeyboardButton("Пушкинский",
                             callback_data="district_pushkinsky"),
        InlineKeyboardButton("Фрунзенский",
                             callback_data="district_frunzensky"),
        InlineKeyboardButton("Центральный", callback_data="district_central"),
    )
    return markup


@pytest.fixture
def inline_keyboard_cuisine():
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


@pytest.fixture
def inline_keyboard_cafe_type():
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("Ресторан", callback_data="type_restaurant"),
        InlineKeyboardButton("Кафе", callback_data="type_cafe"),
        InlineKeyboardButton("Столовая", callback_data="type_canteen")
    )
    return markup


def check_markup_type(type):
    return type == InlineKeyboardMarkup


@pytest.mark.parametrize('markup_type, result', [(InlineKeyboardMarkup, True),
                                                 (ReplyKeyboardMarkup, False)])
def test_expected_values(markup_type, result):
    assert check_markup_type(markup_type) == result


def test_check_instance_district(inline_keyboard_district):
    assert all(
        isinstance(row, List) for row in inline_keyboard_district.keyboard)
    for button in inline_keyboard_district.keyboard:
        assert isinstance(button, List)


@pytest.mark.parametrize("row_index, column_index", [
    (0, 0),
    (0, 1),
    (0, 2),
    (1, 0),
    (1, 1),
    (1, 2),
    (2, 0),
    (2, 1),
    (2, 2),
    (3, 0),
    (3, 1),
    (3, 2),
    (4, 0),
    (4, 1),
    (4, 2),
    (5, 0),
    (5, 1)
])
def test_to_dict_district(row_index, column_index, inline_keyboard_district):
    inline_keyboard_markup_dict = inline_keyboard_district.to_dict()
    assert isinstance(inline_keyboard_markup_dict, dict)
    assert (
            inline_keyboard_markup_dict["inline_keyboard"][row_index][
                column_index]
            == inline_keyboard_district.keyboard[row_index][
                column_index].to_dict()
    )


@pytest.mark.parametrize("row_index, column_index", [
    (0, 0),
    (0, 1),
    (0, 2),
    (1, 0),
    (1, 1),
    (1, 2),
    (2, 0),
    (2, 1)
])
def test_to_dict_cuisine(row_index, column_index, inline_keyboard_cuisine):
    inline_keyboard_markup_dict = inline_keyboard_cuisine.to_dict()
    assert isinstance(inline_keyboard_markup_dict, dict)
    assert (
            inline_keyboard_markup_dict["inline_keyboard"][row_index][
                column_index]
            == inline_keyboard_cuisine.keyboard[row_index][
                column_index].to_dict()
    )


def test_check_instance_cuisine(inline_keyboard_cuisine):
    assert all(
        isinstance(row, List) for row in inline_keyboard_cuisine.keyboard)
    for button in inline_keyboard_cuisine.keyboard:
        assert isinstance(button, List)


@pytest.mark.parametrize("row_index, column_index", [
    (0, 0),
    (0, 1),
    (0, 2)
])
def test_to_dict_cafe(row_index, column_index, inline_keyboard_cafe_type):
    inline_keyboard_markup_dict = inline_keyboard_cafe_type.to_dict()
    assert isinstance(inline_keyboard_markup_dict, dict)
    assert (
            inline_keyboard_markup_dict["inline_keyboard"][row_index][
                column_index]
            == inline_keyboard_cafe_type.keyboard[row_index][
                column_index].to_dict()
    )


def test_check_instance_cafe_type(inline_keyboard_cafe_type):
    assert all(
        isinstance(row, List) for row in inline_keyboard_cafe_type.keyboard)
    for button in inline_keyboard_cafe_type.keyboard:
        assert isinstance(button, List)


def test_response_message():
    data = {
        'link': "test",
        'street': "test",
        'accuracy_address': "test",
        'room_area': 123,
        'room_price': 123,
        'working_hours': "test",
        'delivery': True
    }

    expected = f"""
1. Ссылка на объявление: {data.get("link")}
2. Улица: {data.get("street")}
3. Точный адрес помещения: {data.get("accuracy_address")}
4. Площадь помещения (м2): {data.get("room_area")}
5. Цена за помещение (руб/мес): {data.get("room_price")}
6. Выгодное время работы: {data.get("working_hours")}
7. Возможность доставки: {"Рекомендуется" if data.get("delivery") else "Не влияет"}
"""

    assert create_str_response(data) == expected


def test_markup_inline_cafe_type():
    expected_markup = InlineKeyboardMarkup()
    expected_markup.add(
        InlineKeyboardButton("Ресторан", callback_data="type_restaurant"),
        InlineKeyboardButton("Кафе", callback_data="type_cafe"),
        InlineKeyboardButton("Столовая", callback_data="type_canteen")
    )

    actual_keyboard = markup_inline_cafe_type()
    for row_expected, row_actual in zip(
            expected_markup.to_dict()['inline_keyboard'],
            actual_keyboard.to_dict()['inline_keyboard']):
        for button_expected, button_actual in zip(row_expected, row_actual):
            assert button_expected['callback_data'] == button_actual[
                'callback_data']


def test_markup_inline_district():
    expected_markup = InlineKeyboardMarkup()
    expected_markup.add(
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
    actual_keyboard = markup_inline_district()
    for row_expected, row_actual in zip(
            expected_markup.to_dict()['inline_keyboard'],
            actual_keyboard.to_dict()['inline_keyboard']):
        for button_expected, button_actual in zip(row_expected, row_actual):
            assert button_expected['callback_data'] == button_actual[
                'callback_data']


def test_inline_markup_cuisine():
    expected_markup = InlineKeyboardMarkup()
    expected_markup.add(
        InlineKeyboardButton("Русская", callback_data="cuisine_russia"),
        InlineKeyboardButton("Китайская", callback_data="cuisine_china"),
        InlineKeyboardButton("Японская", callback_data="cuisine_japan"),
        InlineKeyboardButton("Грузинская", callback_data="cuisine_georgia"),
        InlineKeyboardButton("Итальянская", callback_data="cuisine_italy"),
        InlineKeyboardButton("Корейская", callback_data="cuisine_korea"),
        InlineKeyboardButton("Мексиканская", callback_data="cuisine_mexico"),
        InlineKeyboardButton("Узбекская", callback_data="cuisine_uzbekistan")
    )
    actual_keyboard = markup_inline_cuisine()
    for row_expected, row_actual in zip(expected_markup.to_dict()['inline_keyboard'],
                                        actual_keyboard.to_dict()['inline_keyboard']):
        for button_expected, button_actual in zip(row_expected, row_actual):
            assert button_expected['callback_data'] == button_actual[
                'callback_data']
