# Ping-pong (GKE, with Ingress)

Same in-memory app as `3.1/ping-pong`, with one addition: it
returns 200 on the root path `/`, since GKE's Ingress health-checks
each backend there, regardless of which path its real logic lives
on.

## Endpoints

- `GET /` - returns 200 (Ingress health check only).
- `GET /pingpong` - returns `pong <n>` and increments the counter.
- `GET /pings` - returns the current counter value without
  incrementing it.

## Environment variables

- `PORT` - port the server listens on (default `3002`).

The counter is in-memory: it resets to 0 if the pod restarts. See
the exercise-level README for build, push and deploy commands.