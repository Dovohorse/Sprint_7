import allure

from data import urls
from data.orders_payloads import base_order


class TestOrderAccept:

    @allure.title("Курьер может принять заказ")
    def test_accept_order_success(self, http, courier):
        create_resp = http.post(urls.ORDERS, json=base_order(["GREY"]))
        track = create_resp.json()["track"]

        order_resp = http.get(urls.ORDERS_TRACK, params={"t": track})
        order_id = order_resp.json()["order"]["id"]

        resp = http.put(
            urls.ORDERS_ACCEPT_ID(order_id),
            params={"courierId": courier["id"]},
        )

        assert resp.status_code == 200
        assert resp.json().get("ok") is True
