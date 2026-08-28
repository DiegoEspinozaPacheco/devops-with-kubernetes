# Todo backend

Stores todo items in memory. Each todo is a short text (max 140
characters). Shares its Ingress with "Todo app" under path
/todos.

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