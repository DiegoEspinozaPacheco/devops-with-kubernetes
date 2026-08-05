# Log output

Generates a random UUID on startup, keeps it in memory, and
prints it with a timestamp to the logs every 5 seconds. Now
deployed declaratively via manifests/deployment.yaml.

## Run locally
python main.py

## Run in Docker
docker build -t log-output .
docker run log-output

## Deploy to k3d
docker build -t log-output:latest .
k3d image import log-output:latest
kubectl apply -f manifests/deployment.yaml
kubectl logs -f <pod-name>