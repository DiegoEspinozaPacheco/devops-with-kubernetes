# Ping pong

Responds to GET /pingpong with "pong N", where N is a counter
stored in a Postgres database (not in memory). The counter
survives pod restarts, since the data lives in the database's
own persistent volume, managed by a StatefulSet. Shares its
Ingress with the "Log output" application.

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