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

HTML = """
<html>
<head>
<style>
  body {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    margin: 0;
    flex-direction: column;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    background-color: #ffffff;
  }
  h1 {
    font-size: 32px;
    color: #000000;
    margin: 24px 0 16px 0;
    letter-spacing: -0.5px;
  }
  img {
    max-width: 50vw;
    max-height: 40vh;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  }
  p {
    font-size: 24px;
    color: #808080;
    margin: 8px 0 32px 0;
    font-weight: 300;
  }
  #todo-form {
    display: flex;
    gap: 8px;
    margin-bottom: 24px;
  }
  #todo-input {
    padding: 10px 14px;
    font-size: 16px;
    width: 300px;
    border: 1px solid #ccc;
    border-radius: 6px;
    outline: none;
    transition: border-color 0.2s;
  }
  #todo-input:focus {
    border-color: #4a90d9;
  }
  #todo-form button {
    padding: 10px 20px;
    font-size: 16px;
    cursor: pointer;
    border: none;
    border-radius: 6px;
    background-color: #4a90d9;
    color: white;
    transition: background-color 0.2s;
  }
  #todo-form button:hover {
    background-color: #3a7bc0;
  }
  #todo-list {
    list-style: none;
    padding: 0;
    width: 300px;
  }
  #todo-list li {
    padding: 12px;
    margin-bottom: 8px;
    background-color: #f7f7f7;
    border-radius: 6px;
    border-left: 3px solid #4a90d9;
  }
  #char-warning {
    color: #d94a4a;
    font-size: 12px;
    height: 16px;
  }
</style>
</head>
<body>
  <h1>Todo app</h1>
  <img src="/image">
  <p>University of Helsinki</p>

  <form id="todo-form">
    <input id="todo-input" type="text" maxlength="140" placeholder="New todo (max 140 characters)">
    <button type="submit">Send</button>
  </form>
  <div id="char-warning"></div>

  <ul id="todo-list"></ul>

  <script>
    const form = document.getElementById('todo-form');
    const input = document.getElementById('todo-input');
    const warning = document.getElementById('char-warning');
    const list = document.getElementById('todo-list');

    function renderTodos(todos) {
      list.innerHTML = '';
      todos.forEach(todo => {
        const li = document.createElement('li');
        li.textContent = todo.content;
        list.appendChild(li);
      });
    }

    function loadTodos() {
      fetch('/todos')
        .then(res => res.json())
        .then(renderTodos)
        .catch(() => { list.innerHTML = '<li>Could not load todos</li>'; });
    }

    input.addEventListener('input', () => {
      warning.textContent = input.value.length >= 140
        ? 'Max 140 characters reached'
        : '';
    });

    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const content = input.value.trim();
      if (!content) return;

      fetch('/todos', {
        method: 'POST',
        headers: { 'Content-type': 'application/json' },
        body: JSON.stringify({ content })
      })
        .then(res => res.json())
        .then(renderTodos)
        .then(() => { input.value = ''; });
    });

    loadTodos();
  </script>
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
            self.wfile.write(HTML.encode())
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