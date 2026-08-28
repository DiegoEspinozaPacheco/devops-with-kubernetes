# Ping pong

Keeps an in-memory counter of how many times it has been pinged.
Shares its Ingress with the "Log output" application, and
exposes an internal-only endpoint that "Log output" uses to
display the current count. The counter resets whenever the pod
restarts, it is not persisted to disk.

## How to consume
Ping the app, the counter increases by one on each call:
```
GET /pingpong
```
Example response:
```
pong 3
```

Read the raw counter value (intended for internal use by other
pods, not the browser):
```
GET /pings
```
Example response:
```
3
```