import allure
import pytest

from helpers.generator import new_courier_creds
from data import urls


class TestCourierCreate:

    @allure.title("Успешное создание курьера")
    def test_create_courier_success(self, http):
        payload = new_courier_creds()
        resp = http.post(urls.COURIER, data=payload)

        assert resp.status_code == 201
        assert resp.json().get("ok") is True

        # Чистим за собой: логинимся и удаляем созданного курьера
        login_resp = http.post(
            urls.COURIER_LOGIN,
            data={"login": payload["login"], "password": payload["password"]},
        )
        if login_resp.status_code == 200:
            courier_id = login_resp.json().get("id")
            http.delete(urls.COURIER_ID(courier_id))

    @allure.title("Нельзя создать двух курьеров с одинаковым логином")
    def test_create_courier_duplicate_login(self, http):
        payload = new_courier_creds()

        first = http.post(urls.COURIER, data=payload)
        # Если до этого такого логина не было, ожидаем 201; если был — 409
        assert first.status_code in (201, 409)

        second = http.post(urls.COURIER, data=payload)
        assert second.status_code == 409
        assert "Этот логин уже используется" in second.text

        # Чистим за собой на случай, если первый запрос создал курьера
        login_resp = http.post(
            urls.COURIER_LOGIN,
            data={"login": payload["login"], "password": payload["password"]},
        )
        if login_resp.status_code == 200:
            courier_id = login_resp.json().get("id")
            http.delete(urls.COURIER_ID(courier_id))

    @allure.title("Создание курьера без обязательного поля приводит к ошибке 400")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_create_courier_missing_required_field(self, http, missing_field):
        payload = new_courier_creds()
        payload.pop(missing_field)

        resp = http.post(urls.COURIER, data=payload)

        assert resp.status_code == 400
        assert "Недостаточно данных" in resp.text
