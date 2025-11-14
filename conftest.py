import pytest
import requests
import allure

from helpers.generator import new_courier_creds
from data import urls


class HttpClient:
    """HTTP-клиент с сессией requests и шагами Allure."""

    def __init__(self):
        self.session = requests.Session()

    @allure.step("GET {url}")
    def get(self, url, **kwargs):
        return self.session.get(url, **kwargs)

    @allure.step("POST {url}")
    def post(self, url, **kwargs):
        return self.session.post(url, **kwargs)

    @allure.step("PUT {url}")
    def put(self, url, **kwargs):
        return self.session.put(url, **kwargs)

    @allure.step("DELETE {url}")
    def delete(self, url, **kwargs):
        return self.session.delete(url, **kwargs)


@pytest.fixture(scope="session")
def http():
    """HTTP клиент с сессионным requests.Session и шагами Allure."""
    return HttpClient()


@pytest.fixture
def courier(http):
    """Создать курьера перед тестом и удалить после."""
    creds = new_courier_creds()

    # регистрация
    resp_create = http.post(urls.COURIER, data=creds)
    assert resp_create.status_code in (201, 409), (
        f"Не удалось создать курьера: {resp_create.status_code} {resp_create.text}"
    )

    # логин для получения id
    login_body = {"login": creds["login"], "password": creds["password"]}
    resp_login = http.post(urls.COURIER_LOGIN, data=login_body)
    assert resp_login.status_code == 200, (
        f"Не удалось залогиниться курьером: {resp_login.status_code} {resp_login.text}"
    )

    courier_id = resp_login.json().get("id")
    data = {"id": courier_id, **creds}
    yield data

    # удаление курьера после теста
    if courier_id:
        http.delete(urls.COURIER_ID(courier_id))
