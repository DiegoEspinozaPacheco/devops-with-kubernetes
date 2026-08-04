import os
from http.server import HTTPServer, BaseHTTPRequestHandler

FILE_PATH = "/usr/src/app/files/pingpong.txt"
counter = 0

def read_counter():
    global counter
    try:
        with open(FILE_PATH, "r") as f:
            counter = int(f.read().strip())
    except (FileNotFoundError, ValueError):
        counter = 0

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        global counter
        if self.path == "/pingpong":
            body = f"pong {counter}"
            counter += 1
            with open(FILE_PATH, "w") as f:
                f.write(str(counter))
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(body.encode())
        else:
            self.send_response(404)
            self.end_headers()

port = int(os.environ.get("PORT", 3002))

if __name__ == "__main__":
    read_counter()
    print(f"Server started in port {port}", flush=True)
    server = HTTPServer(("0.0.0.0", port), Handler)
    server.serve_forever()