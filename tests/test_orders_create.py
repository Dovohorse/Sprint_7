import allure
import pytest

from data import urls
from data.orders_payloads import base_order


class TestOrdersCreate:

    @allure.title("Можно создать заказ с разными вариантами цвета")
    @pytest.mark.parametrize("colors", [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        [],
    ])
    def test_create_order_colors(self, http, colors):
        color_value = colors if colors else None
        payload = base_order(color_value)

        resp = http.post(urls.ORDERS, json=payload)

        assert resp.status_code == 201
        assert "track" in resp.json()
