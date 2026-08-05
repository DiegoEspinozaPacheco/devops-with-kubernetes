# Todo app

Web server that prints "Server started in port NNNN" on startup.
Port is configurable via the PORT environment variable.

## Run locally
PORT=3000 python main.py

## Run in Docker
docker build -t todo-app .
docker run -e PORT=3000 todo-app

## Deploy to k3d
docker build -t todo-app:latest .
k3d image import todo-app:latest
kubectl create deployment todo-app --image=todo-app:latest
kubectl logs -f <pod-name>