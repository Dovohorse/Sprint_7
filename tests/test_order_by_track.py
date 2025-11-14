import allure

from data import urls
from data.orders_payloads import base_order


class TestOrderByTrack:

    @allure.title("Можно получить заказ по его треку")
    def test_get_order_by_track(self, http):
        create_resp = http.post(urls.ORDERS, json=base_order(["BLACK"]))
        track = create_resp.json()["track"]

        resp = http.get(urls.ORDERS_TRACK, params={"t": track})

        assert resp.status_code == 200
        assert "order" in resp.json()
