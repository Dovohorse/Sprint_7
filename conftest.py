import pytest
import requests

from helpers.generator import new_courier_creds
from data import urls


@pytest.fixture(scope="session")
def http():
    """Сессионный клиент requests."""
    session = requests.Session()
    return session


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
        http.delete(urls.COURIER_ID(courier_id), json={"id": courier_id})
