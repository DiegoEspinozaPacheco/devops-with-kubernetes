# Todo app

Web server that prints "Server started in port NNNN" on startup.
Port is configurable via the PORT environment variable. Now
deployed declaratively via manifests/deployment.yaml.

## Run locally
PORT=3000 python main.py

## Run in Docker
docker build -t todo-app .
docker run -e PORT=3000 todo-app

## Deploy to k3d
docker build -t todo-app:latest .
k3d image import todo-app:latest
kubectl apply -f manifests/deployment.yaml