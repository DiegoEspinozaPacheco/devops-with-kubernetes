# Todo backend

Stores todo items in a Postgres database. Each request is
logged: GET /todos, successful POST /todos, and rejected todos
(over 140 characters, empty, or malformed JSON) are all printed
to stdout, so they can be found in Grafana/Loki filtering by
"REJECTED". Shares its Ingress with "Todo app" under path /todos.

## How to consume
List the current todos:
```
GET /todos
```
Example response:
```
[{"content": "Learn Kubernetes basics"}]
```

Create a new todo (max 140 characters):
```
POST /todos
Content-Type: application/json

{"content": "Buy milk"}
```
Example response, the updated list:
```
[{"content": "Learn Kubernetes basics"}, {"content": "Buy milk"}]
```

Todos over 140 characters, empty, or malformed JSON are rejected
with a 400 and logged as REJECTED.