# Todo app

Web server for the course project. Serves the project UI on GET / and the cached image on GET /image. Port is configurable via the PORT environment variable.

## Features so far
- Server prints "Server started in port X" on startup (1.2)
- Responds to GET / (1.5)
- Exposed via NodePort, then Ingress (1.6, 1.8)
- Displays a random image from Lorem Picsum, cached in a  PersistentVolume for 10 minutes and surviving pod restarts (1.12)
- Todo input field (max 140 characters), send button (not yet
  wired to the backend), and a hardcoded list of todos (1.13)

## Run locally
```
PORT=3000 python main.py
```

## Run in Docker
```
docker build -t todo-app .
docker run -e PORT=3000 -p 3000:3000 todo-app
```

## Deploy to k3d
```
docker build -t todo-app:latest ./todo-app
k3d image import todo-app:latest -c k3s-default
kubectl apply -f persistent-volume
kubectl apply -f todo-app/manifests
```

## Required one-time setup
The PersistentVolume uses a local path on the k3d agent node, create it before applying the manifests:

```
docker exec k3d-k3s-default-agent-0 mkdir -p /tmp/kube-todo
```

## Check status
```
kubectl get pods
kubectl get pv,pvc
```

## Access
Cluster must be created with:

```
k3d cluster create --port 8082:30080@agent:0 -p 8081:80@loadbalancer --agents 2
```

Then open http://localhost:8081

Note: if "Log output" Ingress is also applied, delete it first to avoid routing conflicts, since both currently use path /.

```
kubectl delete ingress log-output-ingress
```