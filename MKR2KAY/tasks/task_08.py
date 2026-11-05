"""МКР. Завдання 08: Безпечний розбір чисел."""



import re


class ParseError(Exception):
    """Помилка розбору числа."""
    pass


def parse_one(text: str) -> float:
    value = text.strip()

    pattern = r"-?\d+(?:\.\d+)?"

    if not re.fullmatch(pattern, value):
        raise ParseError(f"Некоректне число: {text}")

    return float(value)


def parse_numbers(items: list[str]) -> tuple[list[float], list[str]]:
    numbers = []
    errors = []

    for index, text in enumerate(items, start=1):
        try:
            number = parse_one(text)
            numbers.append(number)
        except ParseError as error:
            errors.append(f"Елемент {index}: {error}")

    return numbers, errors
