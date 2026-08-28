import os
import time
import psycopg2
from http.server import HTTPServer, BaseHTTPRequestHandler

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
                "CREATE TABLE IF NOT EXISTS counter (id INTEGER PRIMARY KEY, value INTEGER)"
            )
            cur.execute(
                "INSERT INTO counter (id, value) VALUES (0, 0) ON CONFLICT (id) DO NOTHING"
            )
            conn.commit()
            cur.close()
            conn.close()
            return
        except psycopg2.OperationalError:
            time.sleep(3)
    raise RuntimeError("Could not connect to the database")

def get_and_increment():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT value FROM counter WHERE id = 0")
    value = cur.fetchone()[0]
    cur.execute("UPDATE counter SET value = %s WHERE id = 0", (value + 1,))
    conn.commit()
    cur.close()
    conn.close()
    return value

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/pingpong":
            value = get_and_increment()
            body = f"pong {value}"
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(body.encode())
        elif self.path == "/pings":
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT value FROM counter WHERE id = 0")
            value = cur.fetchone()[0]
            cur.close()
            conn.close()
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(str(value).encode())
        else:
            self.send_response(404)
            self.end_headers()

port = int(os.environ.get("PORT", 3002))

if __name__ == "__main__":
    init_db()
    print(f"Server started in port {port}", flush=True)
    server = HTTPServer(("0.0.0.0", port), Handler)
    server.serve_forever()