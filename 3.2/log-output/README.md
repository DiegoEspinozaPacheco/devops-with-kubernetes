# Log output (GKE, with Ingress)

Two containers sharing a pod, same as `2.1`/`2.3`:

- `log-randomizer`: generates a random string on startup and
  writes it with a timestamp to a shared file every 5 seconds.
- `http-endpoint`: reads that file and, on every request, also
  asks "Ping-pong" (over internal HTTP, `ping-pong-svc`) for its
  current count. It responds with both pieces of information
  together.

## How to consume

Visit the root path to see the latest timestamp, the random
string, and the current ping-pong count:
```
GET /
```
Example response:
```
2026-09-22T20:40:00.000Z: 8523ecb1-c716-4cb6-a044-b9e83bb98e43.
Ping / Pongs: 3
```

This same path also doubles as GKE's Ingress health check for this
service. See the exercise-level README for build, push and deploy
commands.