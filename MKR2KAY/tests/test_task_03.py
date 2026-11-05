"""Відкриті приклади 03 (з картки). Повний набір перевірок — у викладача."""
import copy

import pytest
from conftest import load

M = load(3)

PUBLIC = [('css_winner', (['p', '.note', 'p.note'],), 'Переможець: p.note (0,1,1); номер: 3'),
 ('css_winner',
  (['#intro', 'p#intro.note', 'body #intro'],),
  'Переможець: p#intro.note (1,1,1); номер: 2'),
 ('css_winner', (['p', 'h1, h2'],), ('ValueError', 'Непідтримуваний селектор: h1, h2'))]


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
    for name in ('css_winner',):
        assert callable(getattr(M, name, None)), f"немає функції {name}"
