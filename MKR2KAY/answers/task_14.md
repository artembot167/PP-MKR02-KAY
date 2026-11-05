# Завдання 14. Нескінченні спроби надіслати замовлення (середнє)

Клієнт надсилає замовлення на сервер.

```python
import requests

def send_order(order):
    for attempt in range(1000):
        r = requests.post("https://shop.example/api/orders", json=order)
        if r.status_code != 201:
            continue
        return r.json()
```

**Завдання.** Знайдіть щонайменше чотири проблеми, поясніть, до чого кожна призводить, і опишіть, як побудувати надійні повторні спроби.

**Обсяг:** до 12 речень.

---

Відповідь:

