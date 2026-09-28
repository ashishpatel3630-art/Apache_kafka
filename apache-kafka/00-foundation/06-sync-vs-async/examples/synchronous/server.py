from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import time


HOST = "localhost"
PORT = 8000


class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path != "/process":
            self.send_error(404, "Not Found")
            return

        print("Received request")
        print("Processing request...")

        # Simulate a slow operation
        time.sleep(3)

        response = {
            "status": "success",
            "message": "Task completed",
        }

        body = json.dumps(response).encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()

        self.wfile.write(body)

        print("Response sent")

    def log_message(self, format, *args):
        return


def main():
    server = HTTPServer((HOST, PORT), RequestHandler)

    print(f"Synchronous server running at http://{HOST}:{PORT}")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server...")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()