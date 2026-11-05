"""Відкриті приклади 10 (з картки). Повний набір перевірок — у викладача."""
import pytest
from conftest import load

M = load(10)

PUBLIC = [([{'name': 'Хліб', 'qty': 2, 'price': 25.5}],
  '{\n'
  '  "items": [\n'
  '    {\n'
  '      "name": "Хліб",\n'
  '      "qty": 2,\n'
  '      "price": 25.5,\n'
  '      "total": 51.0\n'
  '    }\n'
  '  ]\n'
  '}')]


@pytest.mark.parametrize("data,expected", PUBLIC)
def test_public(data, expected):
    assert M.records_to_json(data) == expected


def test_functions_exist():
    for name in ('records_to_json', 'json_to_csv'):
        assert callable(getattr(M, name, None)), f"немає функції {name}"
