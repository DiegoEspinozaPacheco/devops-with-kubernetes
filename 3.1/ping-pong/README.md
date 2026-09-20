# Ping-pong (GKE)

Same Ping-pong app as `2.1/ping-pong`, deployed to Google Kubernetes
Engine and exposed with a `LoadBalancer` Service instead of an
Ingress. Uses the in-memory counter version (not the Postgres-backed
version from `2.7`), since this exercise only asks for a
LoadBalancer-exposed deployment.

## Endpoints

- `GET /pingpong` - returns `pong <n>` and increments the counter.
- `GET /pings` - returns the current counter value without
  incrementing it.

## Environment variables

- `PORT` - port the server listens on (default `3002`).

See the exercise-level `README.md` for build, push and deploy
commands.