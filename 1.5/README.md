# Todo app

Web server that responds to GET / and prints "Server started in
port NNNN" on startup. Port is configurable via the PORT
environment variable.

## Run locally
PORT=3000 python main.py

## Run in Docker
docker build -t todo-app .
docker run -e PORT=3000 -p 3000:3000 todo-app

## Deploy to k3d
docker build -t todo-app:latest .
k3d image import todo-app:latest
kubectl apply -f manifests/deployment.yaml

## Access
kubectl port-forward <pod-name> 3000:3000
Then open http://localhost:3000