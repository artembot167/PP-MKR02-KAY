"""Відкриті приклади 02 (з картки). Повний набір перевірок — у викладача."""
import copy

import pytest
from conftest import load

M = load(2)

PUBLIC = [('page_audit',
  ('<!doctype html><html lang="uk"><head><title>Каталог</title><script src="app.js" '
   'defer></script></head><body><h1>Каталог</h1><h2>Книги</h2><img src="a.png" '
   'alt="Обкладинка"><img src="b.png" alt=""></body></html>',),
  []),
 ('page_audit',
  ('<html><head><title>  </title><script src="a.js"></script><script src="b.js" '
   'async></script><script type="module" '
   'src="m.js"></script></head><body><h2>Вступ</h2><h4>Деталі</h4><img '
   'src="x.png"><img><h1>A</h1><h1>B</h1></body></html>',),
  ['Немає заголовка title',
   'Немає атрибута lang у html',
   'Зображення без alt: x.png',
   'Зображення без alt: (без src)',
   'Перший заголовок h2, а не h1',
   'Пропуск рівня заголовка: h2 -> h4',
   'Кілька h1: 2',
   'Блокувальний скрипт у head: a.js']),
 ('page_audit', (5,), ('ValueError', 'Очікується рядок'))]


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
    for name in ('page_audit',):
        assert callable(getattr(M, name, None)), f"немає функції {name}"
