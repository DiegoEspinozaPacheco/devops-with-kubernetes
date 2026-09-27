# Ping-pong (GKE, with Gateway route rewriting)

Same in-memory app as `3.3/ping-pong`, but it no longer knows about
`/pingpong`. All logic now lives on the root path `/`; the
`HTTPRoute` rewrites external `/pingpong` requests to `/` before
they reach this app, so the app stays agnostic of the cluster's
URL structure.

## Endpoints

- `GET /` - returns `pong <n>` and increments the counter. Also
  doubles as GKE's Gateway health check target.
- `GET /pings` - returns the current counter value without
  incrementing it.

## Environment variables

- `PORT` - port the server listens on (default `3002`).

The counter is in-memory: it resets to 0 if the pod restarts. Note
that the load balancer's own periodic health check against `/` also
increments the counter, since `/` is real logic here rather than a
separate no-op health check path. See the exercise-level README for
build, push and deploy commands.