# 2.8 - The project, step 11

Todo backend now stores todos in a Postgres database running as
a StatefulSet (1 replica) in the "project" namespace, instead of
in memory. Credentials are provided via a Secret.

## Check current context and namespace
```
kubectx
kubens
```

## Deploy
```
kubectl apply -f namespaces
kubectl apply -f todo-backend/manifests/secret.yaml
kubectl apply -f postgres/manifests
kubectl apply -f persistent-volume
```

## Build and import images
```
docker build -t todo-app:latest ./todo-app
docker build -t todo-backend:latest ./todo-backend
k3d image import todo-app:latest todo-backend:latest -c k3s-default
```

## Deploy the apps
```
kubectl apply -f todo-app/manifests
kubectl apply -f todo-backend/manifests
```

## Check status
```
kubectl get statefulset -n project
kubectl get pods -n project
kubectl get pvc -n project
```

## Debug the database directly (optional)
A disposable pod with the psql client, deleted automatically on exit:
```
kubectl run -it --rm --restart=Never --image postgres -n project psql-for-debugging -- sh
```
Inside it:
```
psql postgres://todoapp:todoapppass@postgres-svc.project.svc.cluster.local:5432/todos
\dt
SELECT * FROM todos;
```

## View postgres logs
```
kubectl logs postgres-stset-0 -n project
```

## Test
Only one Ingress can serve path / at a time, disable Log
output's if it is currently active:
```
kubectl delete ingress log-output-ingress -n exercises
```
```
curl http://localhost:8081/todos
curl -X POST http://localhost:8081/todos -H "Content-type: application/json" -d '{"content":"Persistent todo"}'
curl http://localhost:8081/todos
```

## Confirm todos survive a pod restart
```
kubectl delete pod -l app=todo-backend -n project
curl http://localhost:8081/todos
```
The todo added earlier should still be there.

## Access
Cluster must be created with:
```
k3d cluster create --port 8082:30080@agent:0 -p 8081:80@loadbalancer --agents 2
```