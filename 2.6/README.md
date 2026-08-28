# 2.6 - The project, step 10

Todo app no longer has hard coded ports, URLs, or paths in its
source code. IMAGE_PATH, CACHE_SECONDS, and PICSUM_URL are now
read from a ConfigMap; PORT stays as a plain env var, as in
every previous exercise.

## Check current context and namespace
```
kubectx
kubens
```

## Deploy
```
kubectl apply -f namespaces
kubectl apply -f persistent-volume
kubectl apply -f todo-app/manifests
kubectl apply -f todo-backend/manifests
```

## Build and import images
```
docker build -t todo-app:latest ./todo-app
docker build -t todo-backend:latest ./todo-backend
k3d image import todo-app:latest todo-backend:latest -c k3s-default
```

## Apply changes to an existing deployment
```
kubectl rollout restart deployment/todo-app -n project
```

## Check the ConfigMap
```
kubectl get configmap -n project
kubectl describe configmap todo-app-config -n project
kubectl exec -it deployment/todo-app -n project -- env | grep -E "IMAGE_PATH|CACHE_SECONDS|PICSUM_URL"
```

## Confirm values actually come from the ConfigMap
Temporarily lower the cache time and watch the picture change
faster than every 10 minutes:
```
kubectl edit configmap todo-app-config -n project
```
Set CACHE_SECONDS to "15", then:
```
kubectl rollout restart deployment/todo-app -n project
```
Refresh http://localhost:8081 every few seconds, the picture
should change roughly every 15 seconds. Afterwards, set
CACHE_SECONDS back to "600" and restart again.

## Test
Only one Ingress can serve path / at a time, disable Log
output's if it is currently active:
```
kubectl delete ingress log-output-ingress -n exercises
```
```
curl http://localhost:8081/
curl http://localhost:8081/todos
```

## Access
Cluster must be created with:
```
k3d cluster create --port 8082:30080@agent:0 -p 8081:80@loadbalancer --agents 2
```