"""Відкриті приклади 05 (з картки). Повний набір перевірок — у викладача."""
import pytest
from conftest import load

M = load(5)


def make(serve, routes):
    def handler(request):
        spec = routes.get(request.path)
        if spec is None:
            return 404, {}, "немає"
        code, headers = spec
        return code, headers, "ok"

    return serve(handler)


def test_public_single_redirect(serve):
    server = make(serve, {"/old": (301, {"Location": "/new"}), "/new": (200, {})})
    assert M.trace_redirects(server.base_url, "/old") == (
        "Крок 1: /old -> 301 -> /new\nКрок 2: /new -> 200\nРезультат: 200; перенаправлень: 1")


def test_public_loop(serve):
    server = make(serve, {"/a": (302, {"Location": "/b"}), "/b": (302, {"Location": "/a"})})
    with pytest.raises(ValueError) as exc:
        M.trace_redirects(server.base_url, "/a")
    assert str(exc.value) == "Цикл перенаправлень: /a"


def test_functions_exist():
    assert callable(getattr(M, "trace_redirects", None)), "немає функції trace_redirects"
