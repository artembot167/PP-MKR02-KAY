"""Відкриті приклади 06 (з картки). Повний набір перевірок — у викладача."""
from conftest import load

M = load(6)


def card(name, price, href):
    return (f'<div class="product"><a class="name" href="{href}">{name}</a>'
            f'<span class="price">{price}</span><span class="stock">В наявності</span></div>')


PAGES = {
    "/catalog": f'<html><body>{card("Кабель", "120 грн", "/item/1")}<a rel="next" href="/catalog?page=2">Далі</a></body></html>',
    "/catalog?page=2": f'<html><body>{card("Миша", "1 299,50 грн", "/item/2")}</body></html>',
}


def make(serve, robots_code, robots_text):
    def handler(request):
        if request.path == "/robots.txt":
            return robots_code, {}, robots_text
        if request.path in PAGES:
            return 200, {}, PAGES[request.path]
        return 404, {}, ""

    return serve(handler)


def test_public_full_crawl(serve):
    server = make(serve, 404, "")
    items = M.scrape_catalog(server.base_url)
    assert items == [
        {"name": "Кабель", "price": 120.0, "in_stock": True, "url": server.base_url + "/item/1"},
        {"name": "Миша", "price": 1299.5, "in_stock": True, "url": server.base_url + "/item/2"},
    ]
    assert server.paths() == ["/robots.txt", "/catalog", "/catalog?page=2"]
    assert all(r.headers.get("user-agent") == "ClassBot/1.0" for r in server.log)


def test_public_robots_disallow(serve):
    server = make(serve, 200, "User-agent: *\nDisallow: /catalog?page=2\n")
    assert [i["name"] for i in M.scrape_catalog(server.base_url)] == ["Кабель"]
    assert "/catalog?page=2" not in server.paths()


def test_functions_exist():
    assert callable(getattr(M, "scrape_catalog", None)), "немає функції scrape_catalog"
