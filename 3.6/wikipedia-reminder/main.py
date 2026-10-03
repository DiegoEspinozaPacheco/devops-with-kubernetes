import os
import json
import http.client
from urllib.parse import urlparse

TODO_BACKEND_URL = os.environ["TODO_BACKEND_URL"]
USER_AGENT = "wikipedia-reminder-bot/1.0 (https://github.com/DiegoEspinozaPacheco/devops-with-kubernetes)"

def get_random_wikipedia_url():
    conn = http.client.HTTPSConnection("en.wikipedia.org")
    conn.request(
        "GET",
        "/wiki/Special:Random",
        headers={"User-Agent": USER_AGENT},
    )
    response = conn.getresponse()
    location = response.getheader("Location")
    conn.close()
    if location and location.startswith("//"):
        location = "https:" + location
    return location

def create_todo(content):
    parsed = urlparse(TODO_BACKEND_URL)
    conn = http.client.HTTPConnection(parsed.hostname, parsed.port)
    body = json.dumps({"content": content})
    conn.request(
        "POST",
        parsed.path,
        body=body,
        headers={"Content-type": "application/json"},
    )
    response = conn.getresponse()
    print(f"Todo created, status {response.status}", flush=True)
    conn.close()

if __name__ == "__main__":
    url = get_random_wikipedia_url()
    print(f"Random Wikipedia article: {url}", flush=True)
    create_todo(f"Read {url}")