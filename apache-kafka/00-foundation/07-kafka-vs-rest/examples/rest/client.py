import json
from urllib.request import Request, urlopen


BASE_URL = "http://127.0.0.1:8000"


def get_order() -> None:
    url = f"{BASE_URL}/orders/101"

    with urlopen(url) as response:
        data = json.loads(response.read().decode("utf-8"))

    print("GET response:")
    print(json.dumps(data, indent=2))


def create_order() -> None:
    url = f"{BASE_URL}/orders"

    payload = {
        "product": "MacBook",
        "quantity": 1,
    }

    request = Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
        },
        method="POST",
    )

    with urlopen(request) as response:
        data = json.loads(response.read().decode("utf-8"))

    print("\nPOST response:")
    print(json.dumps(data, indent=2))


def main() -> None:
    get_order()
    create_order()


if __name__ == "__main__":
    main()