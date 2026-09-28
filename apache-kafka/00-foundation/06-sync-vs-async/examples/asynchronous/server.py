from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import threading
import time


HOST = "localhost"
PORT = 8001


def process_task(task_id: int):
    print(f"[Worker] Processing task {task_id}...")

    time.sleep(3)

    print(f"[Worker] Task {task_id} completed")


class RequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        if self.path != "/tasks":
            self.send_error(404, "Not Found")
            return

        task_id = int(time.time() * 1000)

        worker = threading.Thread(
            target=process_task,
            args=(task_id,),
            daemon=True,
        )

        worker.start()

        response = {
            "status": "accepted",
            "task_id": task_id,
            "message": "Task accepted for background processing",
        }

        body = json.dumps(response).encode("utf-8")

        self.send_response(202)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()

        self.wfile.write(body)

        print(f"[Server] Task {task_id} accepted")

    def log_message(self, format, *args):
        return


def main():
    server = ThreadingHTTPServer((HOST, PORT), RequestHandler)

    print(f"Asynchronous server running at http://{HOST}:{PORT}")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server...")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()