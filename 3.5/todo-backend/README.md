# Todo backend (GKE, Kustomize)

REST API backed by Postgres. Stores and returns todos for `todo-app`.

## Endpoints

- `GET /` - returns `200` with an empty body. Doubles as GKE's
  Gateway health check target.
- `GET /todos` - returns all todos as JSON: `[{"content": "..."}]`
- `POST /todos` - creates a todo from `{"content": "..."}`. Rejects
  (`400`) anything empty or longer than 140 characters; rejected
  attempts are logged.

## Environment variables

- `PORT` - port the server listens on (default `3003`)
- `DB_HOST` - Postgres host
  (`postgres-svc.project.svc.cluster.local`)
- `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD` - from the
  `postgres-credentials` Secret

On startup, retries the database connection for up to 30 seconds
before giving up, to survive Postgres starting slightly later than
this pod.