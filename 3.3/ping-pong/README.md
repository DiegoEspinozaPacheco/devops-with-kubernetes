# Ping-pong (GKE, with Gateway API)

Same in-memory app as `3.2/ping-pong`. It still returns 200 on the
root path `/`, since GKE's Gateway controller health-checks each
backend Service there, the same way its Ingress controller did.

## Endpoints

- `GET /` - returns 200 (Gateway health check only).
- `GET /pingpong` - returns `pong <n>` and increments the counter.
- `GET /pings` - returns the current counter value without
  incrementing it.

## Environment variables

- `PORT` - port the server listens on (default `3002`).

The counter is in-memory: it resets to 0 if the pod restarts. See
the exercise-level README for build, push and deploy commands.