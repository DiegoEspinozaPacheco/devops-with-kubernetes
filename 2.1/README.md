# 2.1 - Connecting pods

Log output and Ping-pong now communicate directly over HTTP
instead of sharing a file on a PersistentVolume. Ping-pong keeps
its request counter in memory and exposes it internally; Log
output fetches it via the cluster's internal DNS and displays it
alongside its own timestamp and random string.

## Disable other apps first
Only one Ingress can serve path / at a time. If "Todo app" is
still deployed from a previous exercise, remove its Ingress:
```
kubectl delete ingress todo-app-ingress
```

## Build and import images
```
docker build -t log-randomizer:latest ./log-output/log-randomizer
docker build -t http-endpoint:latest ./log-output/http-endpoint
docker build -t ping-pong:latest ./ping-pong
k3d image import log-randomizer:latest http-endpoint:latest ping-pong:latest -c k3s-default
```

## Deploy
```
kubectl apply -f log-output/manifests
kubectl apply -f ping-pong/manifests
```

## Check status
```
kubectl get pods
kubectl get svc,ing
```

## Test from outside the cluster
```
curl http://localhost:8081/pingpong
curl http://localhost:8081/
```

## Test internal pod-to-pod communication
```
kubectl apply -f - << 'BUSYBOX'
apiVersion: v1
kind: Pod
metadata:
  name: my-busybox
  labels:
    app: my-busybox
spec:
  containers:
  - image: busybox
    command: ["sleep", "3600"]
    imagePullPolicy: IfNotPresent
    name: busybox
  restartPolicy: Always
BUSYBOX

kubectl exec -it my-busybox -- wget -qO - http://ping-pong-svc:2347/pings
kubectl delete pod/my-busybox
```

## Confirm the counter no longer persists
```
kubectl delete pod -l app=ping-pong
curl http://localhost:8081/
```
The Ping / Pongs count should reset, confirming the data now
lives only in memory, not on the PersistentVolume from 1.11.

## Access
Cluster must be created with:
```
k3d cluster create --port 8082:30080@agent:0 -p 8081:80@loadbalancer --agents 2
```
Then open http://localhost:8081