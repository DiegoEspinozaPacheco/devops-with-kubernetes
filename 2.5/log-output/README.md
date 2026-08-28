# Log output

Two containers sharing a pod:

- log-randomizer: generates a random string on startup and
  writes it with a timestamp to a shared file every 5 seconds.
- http-endpoint: on every request, reads a file and an
  environment variable from a ConfigMap, reads the shared log
  file, and asks the "Ping-pong" application over HTTP for its
  current count. It responds with all of that together.

## How to consume
```
GET /
```
Example response:
```
file content: this text is from file
env variable: MESSAGE=hello world
2026-08-28T17:42:38.739+00:00: 077daf9e-a1a9-4169-b00c-4c2f3134b9b4.
Ping / Pongs: 11
```