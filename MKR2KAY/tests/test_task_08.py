"""Відкриті приклади 08 (з картки). Повний набір перевірок — у викладача."""
import pytest
from conftest import load

M = load(8)

PUBLIC = [((['1', '2.5', 'x'],), ([1.0, 2.5], ['Елемент 3: Некоректне число: x'])), (([],), ([], []))]


@pytest.mark.parametrize("args,expected", PUBLIC)
def test_public(args, expected):
    assert M.parse_numbers(*args) == expected


def test_functions_exist():
    for name in ('ParseError', 'parse_one', 'parse_numbers'):
        assert callable(getattr(M, name, None)), f"немає функції {name}"
