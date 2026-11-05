"""МКР PP. Завдання 01: Розбір HTTP-відповіді."""


def summarize_response(raw: str) -> str:
    if not raw or not raw.strip():
        raise ValueError("Порожня відповідь")

    parts = raw.split("\r\n\r\n", 1)
    header_text = parts[0]
    body = parts[1] if len(parts) > 1 else ""

    lines = header_text.split("\r\n")
    status_line = lines[0].strip()

    status_parts = status_line.split(" ", 2)

    if (
        len(status_parts) < 2
        or not status_parts[0].startswith("HTTP/")
        or len(status_parts[1]) != 3
        or not status_parts[1].isascii()
        or not status_parts[1].isdigit()
    ):
        raise ValueError("Некоректний рядок стану")

    code = int(status_parts[1])

    if not 100 <= code <= 599:
        raise ValueError("Некоректний рядок стану")

    reason = status_parts[2].strip() if len(status_parts) > 2 else ""

    headers = {}

    for line in lines[1:]:
        if not line.strip():
            continue

        if ":" not in line:
            raise ValueError("Некоректний заголовок: " + line)

        name, value = line.split(":", 1)
        name = name.strip().lower()
        value = value.strip()

        if not name:
            raise ValueError("Некоректний заголовок: " + line)

        if name in headers:
            headers[name] += ", " + value
        else:
            headers[name] = value

    content_length = headers.get("content-length")

    if content_length is not None:
        if not content_length.isascii() or not content_length.isdigit():
            raise ValueError("Некоректний Content-Length")

    content_type = headers.get("content-type", "")

    # Прибираємо параметри після крапки з комою
    content_type = content_type.split(";")[0].strip().lower()

    if not content_type:
        content_type = "немає"

    body_length = len(body.encode("utf-8"))

    if content_length is None:
        length_status = "не вказано"
    else:
        length_status = (
            "збігається"
            if int(content_length) == body_length
            else "не збігається"
        )

    classes = {
        1: "інформаційна",
        2: "успіх",
        3: "перенаправлення",
        4: "помилка клієнта",
        5: "помилка сервера",
    }

    status_text = f"{code} {reason}".strip()

    return (
        f"Статус: {status_text} ({classes[code // 100]})\n"
        f"Тип: {content_type}\n"
        f"Довжина тіла: {body_length} байт\n"
        f"Content-Length: {length_status}"
    )

