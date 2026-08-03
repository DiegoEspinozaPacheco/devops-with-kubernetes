import os
from http.server import HTTPServer, BaseHTTPRequestHandler

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ok")

port = int(os.environ.get("PORT", 8000))

if __name__ == "__main__":
    print(f"Server started in port {port}", flush=True)
    server = HTTPServer(("0.0.0.0", port), Handler)
    server.serve_forever()