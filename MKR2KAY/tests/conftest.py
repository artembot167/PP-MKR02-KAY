"""Допоміжні засоби тестів: завантажувач завдань і локальний HTTP-сервер (не змінювати)."""
import importlib.util
import json
import os
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent


def load(number):
    """Повертає модуль завдання з номером number."""
    base = Path(os.environ.get("VARIANT_DIR", ROOT.parent / "tasks"))
    for prefix in ("variant", "lab", "task"):
        path = base / f"{prefix}_{number:02d}.py"
        if path.exists():
            spec = importlib.util.spec_from_file_location(f"{prefix}_{number:02d}", path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
    raise FileNotFoundError(f"Не знайдено файл завдання {number:02d} у {base}")


class LocalServer:
    """Локальний HTTP-сервер на вільному порту. Мережі поза комп'ютером не потрібно.

    handler(request) -> (код, словник заголовків, тіло). Тіло: str, bytes, dict або list (буде JSON).
    request має поля method, path (разом із запитом), headers (імена в нижньому регістрі), body (bytes).
    Усі запити дописуються в журнал log.
    """

    def __init__(self, handler):
        outer = self
        self.log = []

        class Handler(BaseHTTPRequestHandler):
            protocol_version = "HTTP/1.1"

            def _serve(self):
                length = int(self.headers.get("Content-Length") or 0)
                body = self.rfile.read(length) if length else b""
                headers = {k.lower(): v for k, v in self.headers.items()}
                request = type("Request", (), {"method": self.command, "path": self.path,
                                               "headers": headers, "body": body})()
                outer.log.append(request)
                code, extra, payload = handler(request)
                if isinstance(payload, (dict, list)):
                    payload = json.dumps(payload, ensure_ascii=False)
                    extra = {"Content-Type": "application/json; charset=utf-8", **extra}
                if isinstance(payload, str):
                    payload = payload.encode("utf-8")
                payload = payload or b""
                self.send_response(code)
                for key, value in extra.items():
                    self.send_header(key, value)
                if code not in (204, 304):
                    self.send_header("Content-Length", str(len(payload)))
                self.end_headers()
                if code not in (204, 304) and self.command != "HEAD":
                    self.wfile.write(payload)

            do_GET = do_POST = do_PUT = do_PATCH = do_DELETE = do_HEAD = _serve

            def log_message(self, *args):
                pass

        self._httpd = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.base_url = f"http://127.0.0.1:{self._httpd.server_address[1]}"
        self._thread = threading.Thread(target=self._httpd.serve_forever, daemon=True)
        self._thread.start()

    def paths(self):
        return [r.path for r in self.log]

    def close(self):
        self._httpd.shutdown()
        self._httpd.server_close()
        self._thread.join(timeout=5)


@pytest.fixture
def serve():
    """Фабрика серверів: serve(handler) повертає LocalServer; після тесту сервер зупиняється."""
    started = []

    def factory(handler):
        server = LocalServer(handler)
        started.append(server)
        return server

    yield factory
    for server in started:
        server.close()
