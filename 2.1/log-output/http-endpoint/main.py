import os
import urllib.request
from http.server import HTTPServer, BaseHTTPRequestHandler

LOG_PATH = "/usr/src/app/files/log.txt"
PINGPONG_URL = "http://ping-pong-svc:2347/pings"

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            try:
                with open(LOG_PATH, "r") as f:
                    log_content = f.read().strip().splitlines()[-1]
            except (FileNotFoundError, IndexError):
                log_content = "waiting for data..."

            try:
                with urllib.request.urlopen(PINGPONG_URL, timeout=2) as resp:
                    count = resp.read().decode().strip()
            except Exception:
                count = "unavailable"

            body = f"{log_content}.\nPing / Pongs: {count}"
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(body.encode())
        else:
            self.send_response(404)
            self.end_headers()

port = int(os.environ.get("PORT", 3001))

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", port), Handler)
    server.serve_forever()