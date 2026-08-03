import os
from http.server import HTTPServer, BaseHTTPRequestHandler

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<html><body><h1>Todo app</h1></body></html>")
        else:
            self.send_response(404)
            self.end_headers()

port = int(os.environ.get("PORT", 3000))

if __name__ == "__main__":
    print(f"Server started in port {port}", flush=True)
    server = HTTPServer(("0.0.0.0", port), Handler)
    server.serve_forever()