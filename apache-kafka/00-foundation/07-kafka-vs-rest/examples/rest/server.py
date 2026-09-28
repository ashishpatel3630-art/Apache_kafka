
---

# 9. `examples/rest/server.py`

```python
from http.server import BaseHTTPRequestHandler, HTTPServer
import json


HOST = "127.0.0.1"
PORT = 8000


class RequestHandler(BaseHTTPRequestHandler):
    def send_json(self, status_code: int, data: dict) -> None:
        response = json.dumps(data).encode("utf-8")

        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()

        self.wfile.write(response)

    def do_GET(self) -> None:
        if self.path == "/orders/101":
            self.send_json(
                200,
                {
                    "order_id": 101,
                    "status": "PLACED",
                    "customer": "Ashish",
                },
            )
            return

        self.send_json(
            404,
            {
                "error": "Order not found",
            },
        )

    def do_POST(self) -> None:
        if self.path != "/orders":
            self.send_json(
                404,
                {
                    "error": "Route not found",
                },
            )
            return

        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)

        try:
            order = json.loads(body.decode("utf-8"))
        except json.JSONDecodeError:
            self.send_json(
                400,
                {
                    "error": "Invalid JSON",
                },
            )
            return

        self.send_json(
            201,
            {
                "message": "Order created",
                "order": order,
            },
        )

    def log_message(self, format: str, *args) -> None:
        print(f"[REST] {self.address_string()} - {format % args}")


def main() -> None:
    server = HTTPServer((HOST, PORT), RequestHandler)

    print(f"REST server running at http://{HOST}:{PORT}")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server...")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()