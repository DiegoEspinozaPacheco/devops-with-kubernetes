# 2.5 - Documentation and ConfigMaps

Log output now reads configuration from a ConfigMap: a file
(information.txt) mounted as a volume, and an environment
variable (MESSAGE), both displayed together with the usual
output.

## Check current context and namespace
```
kubectx
kubens
```

## Deploy
```
kubectl apply -f namespaces
kubectl apply -f log-output/manifests
kubectl apply -f ping-pong/manifests
```

## Build and import images
```
docker build -t log-randomizer:latest ./log-output/log-randomizer
docker build -t http-endpoint:latest ./log-output/http-endpoint
docker build -t ping-pong:latest ./ping-pong
k3d image import log-randomizer:latest http-endpoint:latest ping-pong:latest -c k3s-default
```

## Apply changes to an existing deployment
Since the image tag stays :latest, a rollout restart is needed
after rebuilding:
```
kubectl rollout restart deployment/log-output -n exercises
```

## Check the ConfigMap
```
kubectl get configmap -n exercises
kubectl describe configmap log-output-config -n exercises
```

## If old pods get stuck in Terminating
```
kubectl get pods -n exercises
kubectl delete pod <pod-name> -n exercises --force --grace-period=0
```

## Test
Only one Ingress can serve path / at a time, disable Todo app's
if it is currently active:
```
kubectl delete ingress todo-app-ingress -n project
```
```
curl http://localhost:8081/
```
Expected output:
```
file content: this text is from file
env variable: MESSAGE=hello world
2026-08-28T17:42:38.739+00:00: 077daf9e-a1a9-4169-b00c-4c2f3134b9b4.
Ping / Pongs: 11
```

## Access
Cluster must be created with:
```
k3d cluster create --port 8082:30080@agent:0 -p 8081:80@loadbalancer --agents 2
```