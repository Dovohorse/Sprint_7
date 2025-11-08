import random
import string


def rand_str(n: int = 10) -> str:
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(n))


def new_courier_creds() -> dict:
    """Сгенерировать случайные данные курьера."""
    return {
        "login": rand_str(),
        "password": rand_str(),
        "firstName": rand_str(),
    }
