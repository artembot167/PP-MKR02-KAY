"""Відкриті приклади 01 (з картки). Повний набір перевірок — у викладача."""
import copy

import pytest
from conftest import load

M = load(1)

PUBLIC = [('summarize_response',
  ('HTTP/1.1 200 OK\r\n'
   'Content-Type: application/json; charset=utf-8\r\n'
   'Content-Length: 9\r\n'
   '\r\n'
   '{"id": 7}',),
  'Статус: 200 OK (успіх)\n'
  'Тип: application/json\n'
  'Довжина тіла: 9 байт\n'
  'Content-Length: збігається'),
 ('summarize_response',
  ('HTTP/1.1 404 Not Found\r\n'
   'Content-Type: text/html;charset=UTF-8\r\n'
   'Content-Length: 6\r\n'
   '\r\n'
   'Привіт',),
  'Статус: 404 Not Found (помилка клієнта)\n'
  'Тип: text/html\n'
  'Довжина тіла: 12 байт\n'
  'Content-Length: не збігається'),
 ('summarize_response', ('FTP/1.1 200 OK',), ('ValueError', 'Некоректний рядок стану'))]


def _call(fn, args):
    return getattr(M, fn)(*copy.deepcopy(args))


def _check(fn, args, expected):
    if isinstance(expected, tuple) and expected and expected[0] == "ValueError":
        with pytest.raises(ValueError) as info:
            _call(fn, args)
        assert str(info.value) == expected[1]
    else:
        assert _call(fn, args) == expected


@pytest.mark.parametrize("fn,args,expected", PUBLIC, ids=[f"p{i}" for i in range(len(PUBLIC))])
def test_public(fn, args, expected):
    _check(fn, args, expected)


def test_functions_exist():
    for name in ('summarize_response',):
        assert callable(getattr(M, name, None)), f"немає функції {name}"
