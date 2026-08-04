import os
from http.server import HTTPServer, BaseHTTPRequestHandler

FILE_PATH = "/usr/src/app/files/log.txt"

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            try:
                with open(FILE_PATH, "r") as f:
                    content = f.read()
            except FileNotFoundError:
                content = "waiting for data...\n"
            self.wfile.write(content.encode())
        else:
            self.send_response(404)
            self.end_headers()

port = int(os.environ.get("PORT", 3001))

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", port), Handler)
    server.serve_forever()