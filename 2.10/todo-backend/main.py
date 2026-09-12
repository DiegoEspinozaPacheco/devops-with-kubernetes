import os
import time
import json
import psycopg2
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = int(os.environ.get("PORT", 3003))
DB_HOST = os.environ["DB_HOST"]
DB_NAME = os.environ["POSTGRES_DB"]
DB_USER = os.environ["POSTGRES_USER"]
DB_PASSWORD = os.environ["POSTGRES_PASSWORD"]

def get_connection():
    return psycopg2.connect(
        host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD
    )

def init_db():
    for attempt in range(10):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(
                "CREATE TABLE IF NOT EXISTS todos (id SERIAL PRIMARY KEY, content TEXT NOT NULL)"
            )
            conn.commit()
            cur.close()
            conn.close()
            return
        except psycopg2.OperationalError:
            time.sleep(3)
    raise RuntimeError("Could not connect to the database")

def get_todos():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT content FROM todos ORDER BY id")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{"content": r[0]} for r in rows]

def add_todo(content):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO todos (content) VALUES (%s)", (content,))
    conn.commit()
    cur.close()
    conn.close()

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/todos":
            print(f"GET /todos from {self.client_address[0]}", flush=True)
            body = json.dumps(get_todos()).encode()
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
                print(
                    f"REJECTED todo (length={len(content)}): {content!r}",
                    flush=True,
                )
                self.send_response(400)
                self.end_headers()
                return

            print(f"POST /todos: {content!r}", flush=True)
            add_todo(content)
            self.send_response(201)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(get_todos()).encode())
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    init_db()
    print(f"Server started in port {PORT}", flush=True)
    server = HTTPServer(("0.0.0.0", PORT), Handler)
    server.serve_forever()