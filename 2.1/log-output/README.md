# Log output

Two containers sharing a pod:

- log-randomizer: generates a random string on startup and
  writes it with a timestamp to a shared file every 5 seconds.
- http-endpoint: reads that file and, on every request, also
  asks the "Ping-pong" application over HTTP for its current
  count. It responds with both pieces of information together.

## How to consume
Visit the root path to see the latest timestamp, the random
string, and the current ping-pong count:
```
GET /
```
Example response:
```
2026-08-10T13:40:00.000Z: 8523ecb1-c716-4cb6-a044-b9e83bb98e43.
Ping / Pongs: 3
```