def base_order(color=None) -> dict:
    """Базовое тело заказа; при необходимости можно передать список цветов."""
    payload = {
        "firstName": "Naruto",
        "lastName": "Uchiha",
        "address": "Konoha, 142 apt.",
        "metroStation": 4,
        "phone": "+7 800 355 35 35",
        "rentTime": 5,
        "deliveryDate": "2020-06-06",
        "comment": "Ichiraku ramen!",
    }
    if color is not None:
        payload["color"] = color
    return payload
