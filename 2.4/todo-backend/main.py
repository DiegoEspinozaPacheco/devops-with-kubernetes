import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = int(os.environ.get("PORT", 3003))
todos = []

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/todos":
            body = json.dumps(todos).encode()
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/todos":
            length = int(self.headers.get("Content-Length", 0))
            raw = self.rfile.read(length)
            try:
                data = json.loads(raw)
                content = data.get("content", "").strip()
            except json.JSONDecodeError:
                content = ""

            if not content or len(content) > 140:
                self.send_response(400)
                self.end_headers()
                return

            todos.append({"content": content})
            self.send_response(201)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(todos).encode())
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    print(f"Server started in port {PORT}", flush=True)
    server = HTTPServer(("0.0.0.0", PORT), Handler)
    server.serve_forever()