"""Відкриті приклади 09 (з картки). Повний набір перевірок — у викладача."""
import pytest
from conftest import load

M = load(9)

PUBLIC = [('INFO;auth;120\nERROR;auth;300\nWARN;db;50\n',
  ({'auth': {'count': 2, 'avg_ms': 210.0, 'max_ms': 300},
    'db': {'count': 1, 'avg_ms': 50.0, 'max_ms': 50}},
   [])),
 ('INFO;a\nDEBUG;a;5\n;;\nINFO;;5\nINFO;a;x\n',
  ({},
   ['Рядок 1: очікується 3 поля',
    'Рядок 2: некоректний рівень',
    'Рядок 3: некоректний рівень',
    'Рядок 4: порожній сервіс',
    'Рядок 5: некоректний час']))]


@pytest.mark.parametrize("content,expected", PUBLIC)
def test_public(tmp_path, content, expected):
    path = tmp_path / "app.log"
    path.write_text(content, encoding="utf-8")
    assert M.summarize_log(str(path)) == expected


def test_functions_exist():
    for name in ('summarize_log',):
        assert callable(getattr(M, name, None)), f"немає функції {name}"
