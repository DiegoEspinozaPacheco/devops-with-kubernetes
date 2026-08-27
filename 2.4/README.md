# 2.4 - The project, step 9

This exercise asks to move everything related to the project
into a namespace called "project". This was already done as
part of 2.3, where both namespaces ("exercises" and "project")
were created together. No new infrastructure changes are
required here; this snapshot confirms the project's current
state, fully running in the "project" namespace.

## Check current namespace/context
```
kubectx
kubens
```

## Confirm the project resources live in "project"
```
kubectl get all -n project
kubectl get pv,pvc -n project
```

## Deploy (if starting from a clean cluster)
```
kubectl apply -f namespaces
docker exec k3d-k3s-default-agent-0 mkdir -p /tmp/kube-todo
kubectl apply -f persistent-volume
docker build -t todo-app:latest ./todo-app
docker build -t todo-backend:latest ./todo-backend
k3d image import todo-app:latest todo-backend:latest -c k3s-default
kubectl apply -f todo-backend/manifests
kubectl apply -f todo-app/manifests
```

## Test
Only one Ingress can serve path / at a time, disable Log output's
if it is currently active:
```
kubectl delete ingress log-output-ingress -n exercises
```
```
curl http://localhost:8081/
curl http://localhost:8081/todos
curl -X POST http://localhost:8081/todos -H "Content-type: application/json" -d '{"content":"Test todo"}'
curl http://localhost:8081/todos
```

## Access
Cluster must be created with:
```
k3d cluster create --port 8082:30080@agent:0 -p 8081:80@loadbalancer --agents 2
```