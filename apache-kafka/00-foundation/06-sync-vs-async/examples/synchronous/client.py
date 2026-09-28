import urllib.request
import time
import json


URL = "http://localhost:8000/process"


def main():
    print("Sending request...")

    start = time.perf_counter()

    with urllib.request.urlopen(URL) as response:
        data = json.loads(response.read().decode("utf-8"))

    elapsed = time.perf_counter() - start

    print("Response received:")
    print(data)
    print(f"Time taken: {elapsed:.2f} seconds")

    print("Client can continue now.")


if __name__ == "__main__":
    main()