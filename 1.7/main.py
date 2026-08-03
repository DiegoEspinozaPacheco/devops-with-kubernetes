import os
import time
import uuid
import threading
from datetime import datetime, timezone
from http.server import HTTPServer, BaseHTTPRequestHandler

random_string = str(uuid.uuid4())

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            timestamp = datetime.now(timezone.utc).isoformat(timespec="milliseconds")
            body = f"{timestamp}: {random_string}"
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(body.encode())
        else:
            self.send_response(404)
            self.end_headers()

def log_loop():
    while True:
        timestamp = datetime.now(timezone.utc).isoformat(timespec="milliseconds")
        print(f"{timestamp}: {random_string}", flush=True)
        time.sleep(5)

if __name__ == "__main__":
    threading.Thread(target=log_loop, daemon=True).start()
    port = int(os.environ.get("PORT", 3001))
    server = HTTPServer(("0.0.0.0", port), Handler)
    server.serve_forever()