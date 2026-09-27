# Log output (GKE, with Gateway route rewriting)

Same two-container app as `3.3/log-output`, unchanged:

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
2026-09-26T22:00:00.000Z: 8523ecb1-c716-4cb6-a044-b9e83bb98e43.
Ping / Pongs: 3
```

This same path also doubles as the health check that GKE's Gateway
controller runs against this Service. See the exercise-level
README for build, push and deploy commands.