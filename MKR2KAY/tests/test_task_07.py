"""Відкриті приклади 07 (з картки). Повний набір перевірок — у викладача."""
import copy

import pytest
from conftest import load

M = load(7)

PUBLIC = [('revenue_by_city',
  ({'status': 'ok',
    'data': [{'id': 1,
              'status': 'paid',
              'customer': {'name': 'X', 'city': 'Київ'},
              'items': [{'sku': 'S', 'qty': 2, 'price_kop': 15000},
                        {'sku': 'S', 'qty': 1, 'price_kop': 9990, 'discount': 10}]},
             {'id': 2,
              'status': 'cancelled',
              'customer': {'name': 'X', 'city': 'Львів'},
              'items': [{'sku': 'S', 'qty': 1, 'price_kop': 15000}]},
             {'id': 3,
              'status': 'paid',
              'customer': {'name': 'X', 'city': 'Львів'},
              'items': [{'sku': 'S', 'qty': 3, 'price_kop': 5000}]},
             {'id': 4,
              'status': 'paid',
              'customer': None,
              'items': [{'sku': 'S', 'qty': 1, 'price_kop': 20000}]}]},),
  ['Київ: 1 замовл., 389,91 грн',
   'Невідомо: 1 замовл., 200,00 грн',
   'Львів: 1 замовл., 150,00 грн',
   'Усього: 3 замовл., 739,91 грн']),
 ('revenue_by_city', ({'status': 'error', 'data': []},), ('ValueError', 'Помилка API: error')),
 ('revenue_by_city',
  ({'status': 'ok',
    'data': [{'id': 1,
              'status': 'pending',
              'customer': {'name': 'X', 'city': 'Київ'},
              'items': [{'sku': 'S', 'qty': 1, 'price_kop': 100}]}]},),
  ['Немає оплачених замовлень'])]


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
    for name in ('revenue_by_city',):
        assert callable(getattr(M, name, None)), f"немає функції {name}"
