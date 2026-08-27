# 2.3 - Keep them separated

Two namespaces are introduced: "exercises" (Log output,
Ping-pong) and "project" (Todo app, Todo backend). Only one
Ingress can serve path / at a time, so Log output's and Todo
app's Ingress must be applied one at a time, whichever is being
tested.

## Check current context and namespace
```
kubectx
kubens
```

## Create namespaces
```
kubectl apply -f namespaces
kubectl get namespaces
```

## Remove old resources from default namespace
```
kubectl delete deployment log-output ping-pong todo-app todo-backend -n default
kubectl delete ingress log-output-ingress todo-app-ingress -n default
kubectl delete service log-output-svc ping-pong-svc todo-app-svc todo-backend-svc -n default
kubectl delete -f persistent-volume -n default
```

## If the PVC is stuck in Pending or the PV in Terminating
A local PersistentVolume from a previous namespace cannot be
automatically rebound. Force delete it and recreate:
```
kubectl patch pv todo-app-pv -p '{"metadata":{"finalizers":null}}'
kubectl delete pvc todo-app-claim -n project
docker exec k3d-k3s-default-agent-0 rm -rf /tmp/kube-todo
docker exec k3d-k3s-default-agent-0 mkdir -p /tmp/kube-todo
kubectl apply -f persistent-volume
kubectl get pv,pvc -n project
```

## Build and import images
```
docker build -t log-randomizer:latest ./log-output/log-randomizer
docker build -t http-endpoint:latest ./log-output/http-endpoint
docker build -t ping-pong:latest ./ping-pong
docker build -t todo-app:latest ./todo-app
docker build -t todo-backend:latest ./todo-backend
k3d image import log-randomizer:latest http-endpoint:latest ping-pong:latest todo-app:latest todo-backend:latest -c k3s-default
```

## Deploy everything
```
kubectl apply -f log-output/manifests
kubectl apply -f ping-pong/manifests
kubectl apply -f todo-app/manifests
kubectl apply -f todo-backend/manifests
```

## Check status
```
kubectl get pods -n exercises
kubectl get pods -n project
kubectl get pv,pvc -n project
kubectl get all --all-namespaces
```

## Test the "exercises" namespace (Log output + Ping-pong)
Only one Ingress can serve path / at a time, disable Todo app's:
```
kubectl delete ingress todo-app-ingress -n project
kubectl apply -f log-output/manifests
```
```
curl http://localhost:8081/pingpong
curl http://localhost:8081/pingpong
curl http://localhost:8081/
```

## Test the "project" namespace (Todo app + Todo backend)
Disable Log output's Ingress first:
```
kubectl delete ingress log-output-ingress -n exercises
kubectl apply -f todo-app/manifests
```
```
curl http://localhost:8081/
curl http://localhost:8081/todos
curl -X POST http://localhost:8081/todos -H "Content-type: application/json" -d '{"content":"Test todo"}'
curl http://localhost:8081/todos
```

## Switch default namespace with kubens (optional convenience)
```
kubens exercises
kubectl get pods
kubens project
kubectl get pods
kubens default
```

## Access
Cluster must be created with:
```
k3d cluster create --port 8082:30080@agent:0 -p 8081:80@loadbalancer --agents 2
```