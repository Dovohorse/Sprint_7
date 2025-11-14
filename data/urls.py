BASE = "https://qa-scooter.praktikum-services.ru"

COURIER = f"{BASE}/api/v1/courier"
COURIER_LOGIN = f"{BASE}/api/v1/courier/login"


def COURIER_ID(courier_id):
    return f"{BASE}/api/v1/courier/{courier_id}"


ORDERS = f"{BASE}/api/v1/orders"


def ORDERS_ACCEPT_ID(order_id):
    return f"{BASE}/api/v1/orders/accept/{order_id}"


ORDERS_TRACK = f"{BASE}/api/v1/orders/track"
