# Log output

Generates a random UUID on startup, keeps it in memory, prints it
with a timestamp to the logs every 5 seconds, and serves the same
value over HTTP on GET /.

## Run locally
```
PORT=3001 python main.py
```

## Run in Docker
```
docker build -t log-output .
docker run -e PORT=3001 -p 3001:3001 log-output
```

## Deploy to k3d
```
docker build -t log-output:latest .
k3d image import log-output:latest
kubectl apply -f manifests
```

## Access

Cluster must be created with:

```
k3d cluster create --port 8082:30080@agent:0 -p 8081:80@loadbalancer --agents 2
```

Then open http://localhost:8081

## Logs

```
kubectl logs -f <pod-name>
```