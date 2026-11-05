"""МКР PP. Завдання 07: Виторг за містами."""



def revenue_by_city(payload: dict) -> list[str]:
    if payload.get("status") != "ok":
        status = payload.get("status")
        raise ValueError(f"Помилка API: {status}")

    orders = payload.get("data")

    if not isinstance(orders, list):
        raise ValueError("Немає даних")

    seen_ids = set()
    cities = {}

    for order in orders:
        order_id = order["id"]

        if order_id in seen_ids:
            continue

        seen_ids.add(order_id)

        if order.get("status") != "paid":
            continue

        total = 0

        for item in order["items"]:
            qty = item["qty"]
            price = item["price_kop"]
            discount = item.get("discount", 0)

            if (
                qty <= 0
                or price < 0
                or not 0 <= discount <= 100
            ):
                raise ValueError(
                    f"Некоректна позиція в замовленні {order_id}"
                )

            total += qty * price * (100 - discount) // 100

        customer = order.get("customer")

        if not isinstance(customer, dict):
            city = "Невідомо"
        else:
            city = customer.get("city") or "Невідомо"

        if city not in cities:
            cities[city] = {"count": 0, "sum": 0}

        cities[city]["count"] += 1
        cities[city]["sum"] += total

    if not cities:
        return ["Немає оплачених замовлень"]

    sorted_cities = sorted(
        cities.items(),
        key=lambda item: (-item[1]["sum"], item[0])
    )

    result = []
    total_count = 0
    total_sum = 0

    def format_money(kopecks):
        hryvnias = kopecks // 100
        kop = kopecks % 100
        return f"{hryvnias:,}".replace(",", " ") + f",{kop:02d}"

    for city, info in sorted_cities:
        count = info["count"]
        amount = info["sum"]

        total_count += count
        total_sum += amount

        result.append(
            f"{city}: {count} замовл., {format_money(amount)} грн"
        )

    result.append(
        f"Усього: {total_count} замовл., "
        f"{format_money(total_sum)} грн"
    )

    return result
