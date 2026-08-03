import os
from http.server import HTTPServer, BaseHTTPRequestHandler

counter = 0

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        global counter
        if self.path == "/pingpong":
            body = f"pong {counter}"
            counter += 1
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(body.encode())
        else:
            self.send_response(404)
            self.end_headers()

port = int(os.environ.get("PORT", 3002))

if __name__ == "__main__":
    print(f"Server started in port {port}", flush=True)
    server = HTTPServer(("0.0.0.0", port), Handler)
    server.serve_forever()