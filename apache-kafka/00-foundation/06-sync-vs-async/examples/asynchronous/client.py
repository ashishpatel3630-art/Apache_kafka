import urllib.request
import urllib.error
import json
import time


URL = "http://localhost:8001/tasks"


def submit_task():
    request = urllib.request.Request(
        URL,
        method="POST",
        data=b"",
        headers={
            "Content-Type": "application/json",
        },
    )

    start = time.perf_counter()

    with urllib.request.urlopen(request) as response:
        data = json.loads(response.read().decode("utf-8"))

    elapsed = time.perf_counter() - start

    print("Server response:")
    print(data)
    print(f"Request completed in {elapsed:.2f} seconds")


def main():
    print("Submitting task...")

    submit_task()

    print("\nClient continues immediately.")

    for i in range(3):
        print(f"Client doing other work {i + 1}")
        time.sleep(0.5)

    print("\nClient finished its own work.")


if __name__ == "__main__":
    main()