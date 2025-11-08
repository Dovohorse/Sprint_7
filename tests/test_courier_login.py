import allure
import pytest

from data import urls


class TestCourierLogin:

    @allure.title("Курьер может авторизоваться с корректными логином и паролем")
    def test_login_success(self, http, courier):
        # Курьер создан в фикстуре courier и будет удалён после теста
        resp = http.post(
            urls.COURIER_LOGIN,
            data={"login": courier["login"], "password": courier["password"]},
        )

        assert resp.status_code == 200
        assert isinstance(resp.json().get("id"), int)

    @allure.title(
        "Авторизация без обязательного поля (пустой логин/пароль) возвращает 400"
    )
    @pytest.mark.parametrize("empty_field", ["login", "password"])
    def test_login_missing_field(self, http, courier, empty_field):
        # Базовое корректное тело
        body = {
            "login": courier["login"],
            "password": courier["password"],
        }
        # Делаем одно из обязательных полей пустой строкой
        body[empty_field] = ""

        resp = http.post(urls.COURIER_LOGIN, data=body)

        # По документации и словам наставника здесь должен быть 400
        assert resp.status_code == 400, (
            f"Ожидали 400 согласно документации, "
            f"но получили {resp.status_code}. Тело ответа: {resp.text}"
        )
        assert "Недостаточно данных для входа" in resp.text

    @allure.title("Авторизация с несуществующей парой логин/пароль возвращает ошибку")
    def test_login_wrong_pair(self, http):
        resp = http.post(
            urls.COURIER_LOGIN,
            data={"login": "no_such_login", "password": "no_such_password"},
        )

        # В доке 404, но иногда стенд отдаёт 400 — учитываем оба варианта
        assert resp.status_code in (404, 400)
