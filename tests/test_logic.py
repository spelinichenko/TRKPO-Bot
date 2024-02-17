from itertools import product

from telebot.types import Message

from src.enums import CafeType, Cuisine, District
from src.handlers.logic import logic_message


def generate_test_cases():
    test_cases = []

    # Generate all combinations of districts, cuisines, and cafe types
    combinations = product(District, Cuisine, CafeType)

    for combo in combinations:
        district, cuisine, cafe_type = combo
        test_case_str = f"1. {district.value}\n2. {cuisine.value}\n3. {cafe_type.value}"
        test_cases.append(test_case_str)

    return test_cases


async def test_logic_message(test_input, expected):
    test_cases = generate_test_cases()
    for test_case in test_cases[:5]:  # Print first 5 test cases to keep the output manageable
        print(test_case)
        print("---")
