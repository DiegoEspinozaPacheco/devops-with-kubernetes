import os
import time
import urllib.request
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = int(os.environ.get("PORT", 3000))
IMAGE_PATH = "/usr/src/app/files/image.jpg"
CACHE_SECONDS = 600  # 10 minutes

def image_is_stale():
    if not os.path.exists(IMAGE_PATH):
        return True
    age = time.time() - os.path.getmtime(IMAGE_PATH)
    return age > CACHE_SECONDS

def refresh_image():
    urllib.request.urlretrieve("https://picsum.photos/1200", IMAGE_PATH)

HTML = b"""
<html>
<head>
<style>
  body {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    margin: 0;
    flex-direction: column;
    font-family: sans-serif;
  }
  h1 {
    font-size: 32px;
    color: #000000;
    margin: 0 0 12px 0;
  }
  img {
    max-width: 90vw;
    max-height: 70vh;
  }
  p {
    font-size: 24px;
    color: #808080;
    margin: 12px 0 0 0;
  }
</style>
</head>
<body>
  <h1>Todo app</h1>
  <img src="/image">
  <p>University of Helsinki</p>
</body>
</html>
"""

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            if image_is_stale():
                refresh_image()
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(HTML)
        elif self.path == "/image":
            if image_is_stale():
                refresh_image()
            self.send_response(200)
            self.send_header("Content-type", "image/jpeg")
            self.end_headers()
            with open(IMAGE_PATH, "rb") as f:
                self.wfile.write(f.read())
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    print(f"Server started in port {PORT}", flush=True)
    server = HTTPServer(("0.0.0.0", PORT), Handler)
    server.serve_forever()