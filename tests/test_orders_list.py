import allure

from data import urls


class TestOrdersList:

    @allure.title("Запрос списка заказов возвращает массив orders")
    def test_orders_list_returns_orders_array(self, http):
        resp = http.get(urls.ORDERS, params={"limit": 10, "page": 0})

        assert resp.status_code == 200
        body = resp.json()
        assert "orders" in body
        assert isinstance(body["orders"], list)
