# Ping pong

Web server that responds to GET /pingpong with "pong N", where N
is an in-memory counter that increases on every request. The
counter resets if the pod restarts. Shares Ingress with the
"Log output" application.

## Run locally
```
PORT=3002 python main.py
```

## Run in Docker
```
docker build -t ping-pong .
docker run -e PORT=3002 -p 3002:3002 ping-pong
```

## Deploy to k3d
```
docker build -t ping-pong:latest .
k3d image import ping-pong:latest
kubectl apply -f manifests/deployment.yaml
kubectl apply -f manifests/service.yaml
```

Ingress is defined in the "Log output" application manifests,
since both apps share the same Ingress resource.

## Access
Cluster must be created with:
```
k3d cluster create --port 8082:30080@agent:0 -p 8081:80@loadbalancer --agents 2
```

Then open http://localhost:8081/pingpong