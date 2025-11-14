import allure

from helpers.generator import new_courier_creds
from data import urls


class TestCourierDelete:

    @allure.title("Курьера можно удалить")
    def test_delete_courier_success(self, http):
        creds = new_courier_creds()
        http.post(urls.COURIER, data=creds)
        login_resp = http.post(
            urls.COURIER_LOGIN,
            data={"login": creds["login"], "password": creds["password"]},
        )
        courier_id = login_resp.json()["id"]

        resp = http.delete(urls.COURIER_ID(courier_id))

        assert resp.status_code == 200
        assert resp.json().get("ok") is True

    @allure.title("Удаление несуществующего курьера возвращает ошибку")
    def test_delete_courier_not_found(self, http):
        fake_id = 999999
        resp = http.delete(urls.COURIER_ID(fake_id))

        assert resp.status_code in (404, 400)
