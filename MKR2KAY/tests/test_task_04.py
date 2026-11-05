"""Відкриті приклади 04 (з картки). Повний набір перевірок — у викладача."""
import copy

import pytest
from conftest import load

M = load(4)

PUBLIC = [(('<button id="go" onclick="run()">Старт</button><p id="out"></p>',
   'document.getElementById("go").addEventListener("click", start);\n'
   'document.querySelector(\'#out\').textContent = "ok";\n'
   "document.getElementById('missing').hidden = true;"),
  ['Немає елемента #missing', 'Вбудований обробник onclick у <button>']),
 (('<div id="a"></div><div id="a"></div><input id="b" ONINPUT="x()">',
   'document.querySelector("#a"); document.querySelector("#b");'),
  ['Дубль id: a', 'Вбудований обробник oninput у <input>']),
 ((None, ''), ('ValueError', 'Очікується рядок'))]


def _check(args, expected):
    if isinstance(expected, tuple) and expected and expected[0] == "ValueError":
        with pytest.raises(ValueError) as info:
            M.check_script(*copy.deepcopy(args))
        assert str(info.value) == expected[1]
    else:
        assert M.check_script(*copy.deepcopy(args)) == expected


@pytest.mark.parametrize("args,expected", PUBLIC)
def test_public(args, expected):
    _check(args, expected)


def test_functions_exist():
    for name in ('check_script',):
        assert callable(getattr(M, name, None)), f"немає функції {name}"
