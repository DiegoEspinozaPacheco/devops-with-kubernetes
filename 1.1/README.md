# Log output

Generates a random UUID on startup, keeps it in memory, and
prints it with a timestamp to the logs every 5 seconds.

## Run locally
python main.py

## Run in Docker
docker build -t log-output .
docker run log-output

## Deploy to k3d
docker build -t log-output:latest .
k3d image import log-output:latest
kubectl create deployment log-output --image=log-output:latest
kubectl logs -f <pod-name>