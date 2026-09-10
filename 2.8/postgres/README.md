# Postgres

Database used by the "Todo backend" application to store todos.
Runs as a StatefulSet with a single replica and a dynamically
provisioned volume (local-path), so data survives pod restarts.
Exposed internally via a headless Service (postgres-svc), not
reachable from outside the cluster.

## How to consume
Not consumed via HTTP. Other pods in the "project" namespace
connect to it directly with a Postgres client, using the
credentials from the postgres-credentials Secret:
```
postgres://<user>:<password>@postgres-svc.project.svc.cluster.local:5432/<database>
```