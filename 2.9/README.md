# 2.9 - The project, step 12

A CronJob runs every hour, fetches a random Wikipedia article
URL, and creates a new todo "Read <URL>" via todo-backend.

## Check current context and namespace
```
kubectx
kubens
```

## Build and import image
```
docker build -t wikipedia-reminder:latest ./wikipedia-reminder
k3d image import wikipedia-reminder:latest -c k3s-default
```

## Deploy
```
kubectl apply -f wikipedia-reminder/manifests
```

## Check status
```
kubectl get cronjob -n project
kubectl get jobs -n project
```

## Test without waiting for the schedule
```
kubectl create job --from=cronjob/wikipedia-reminder -n project wikipedia-reminder-manual
kubectl get pods -n project
kubectl logs <job-pod-name> -n project
kubectl delete job wikipedia-reminder-manual -n project
```

## Confirm the todo was created
Only one Ingress can serve path / at a time, disable Log
output's if it is currently active:
```
kubectl delete ingress log-output-ingress -n exercises
```
```
curl http://localhost:8081/todos
```

## Debug the database directly (optional)
```
kubectl run -it --rm --restart=Never --image postgres -n project psql-for-debugging -- sh
```
Inside it:
```
psql postgres://todoapp:todoapppass@postgres-svc.project.svc.cluster.local:5432/todos
SELECT * FROM todos;
```

## Access
Cluster must be created with:
```
k3d cluster create --port 8082:30080@agent:0 -p 8081:80@loadbalancer --agents 2
```