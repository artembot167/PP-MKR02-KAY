"""МКР PP. Завдання 03: Який CSS-селектор переможе."""

import re


def css_winner(selectors: list[str]) -> str:
    if not selectors:
        raise ValueError("Порожній список")

    for selector in selectors:
        s = selector.strip()
        if not s:
            raise ValueError("Порожній селектор")
        if "(" in s or "," in s:
            raise ValueError(f"Непідтримуваний селектор: {s}")

    def specificity(selector):
        # Забираємо вміст атрибутів, але сам атрибут рахуємо
        attrs = re.findall(r'\[[^\]]*\]', selector)
        s = re.sub(r'\[[^\]]*\]', ' ', selector)

        # Псевдоелементи мають вагу як звичайні елементи
        pseudo_elements = re.findall(r'::[a-zA-Z-]+', s)
        s = re.sub(r'::[a-zA-Z-]+', ' ', s)

        ids = re.findall(r'#[a-zA-Z_][\w-]*', s)
        s = re.sub(r'#[a-zA-Z_][\w-]*', ' ', s)

        classes = re.findall(r'\.[a-zA-Z_][\w-]*', s)
        s = re.sub(r'\.[a-zA-Z_][\w-]*', ' ', s)

        pseudo_classes = re.findall(r':[a-zA-Z-]+', s)
        s = re.sub(r':[a-zA-Z-]+', ' ', s)

        # Прибираємо комбінатори та універсальний селектор
        s = re.sub(r'[>+~*]', ' ', s)

        elements = re.findall(r'[a-zA-Z][\w-]*', s)

        a = len(ids)
        b = len(classes) + len(attrs) + len(pseudo_classes)
        c = len(elements) + len(pseudo_elements)

        return (a, b, c)

    winner = max(
        range(len(selectors)),
        key=lambda i: (specificity(selectors[i]), i)
    )

    selector = selectors[winner].strip()
    a, b, c = specificity(selector)

    return f"Переможець: {selector} ({a},{b},{c}); номер: {winner + 1}"
