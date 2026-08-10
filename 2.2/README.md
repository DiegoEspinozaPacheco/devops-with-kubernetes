# 2.2 - The project, step 8

Todo app now talks to a new todo-backend service. Todo app keeps
serving the HTML/JS and the cached picture; the browser calls
todo-backend directly for listing and creating todos (SPA style).

## If the PVC is stuck in Pending
This happens if the cluster/PVC was deleted since 1.12. A local
PersistentVolume cannot be automatically rebound once released,
so the PV must be deleted and recreated:
```
kubectl delete -f persistent-volume
docker exec k3d-k3s-default-agent-0 mkdir -p /tmp/kube-todo
kubectl apply -f persistent-volume
```

## Disable other apps' Ingress first
Only one Ingress can serve path / at a time.
```
kubectl delete ingress log-output-ingress
```

## Build and import images
```
docker build -t todo-app:latest ./todo-app
docker build -t todo-backend:latest ./todo-backend
k3d image import todo-app:latest todo-backend:latest -c k3s-default
```

## Deploy
```
kubectl apply -f persistent-volume
kubectl apply -f todo-backend/manifests
kubectl apply -f todo-app/manifests
```

## Check status
```
kubectl get pods
kubectl get pv,pvc
kubectl get svc,ing
kubectl describe ingress todo-app-ingress
```

## Test todo-backend directly
```
curl http://localhost:8081/todos
curl -X POST http://localhost:8081/todos -H "Content-type: application/json" -d '{"content":"Test todo"}'
curl http://localhost:8081/todos
```

## Test in the browser
Open http://localhost:8081, enter a todo (max 140 characters),
click Send. The new todo should appear in the list without
reloading the page.

## Access
Cluster must be created with:
```
k3d cluster create --port 8082:30080@agent:0 -p 8081:80@loadbalancer --agents 2
```