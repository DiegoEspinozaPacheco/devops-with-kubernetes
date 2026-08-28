# 2.7 - Stateful applications

Ping-pong's counter is now stored in a Postgres database running
as a StatefulSet (1 replica), instead of in memory. The counter
survives pod restarts of both ping-pong and postgres itself.

## Check current context and namespace
```
kubectx
kubens
```

## Deploy
```
kubectl apply -f namespaces
kubectl apply -f ping-pong/manifests/secret.yaml
kubectl apply -f postgres/manifests
```

## Build and import image
```
docker build -t ping-pong:latest ./ping-pong
k3d image import ping-pong:latest -c k3s-default
```

## Deploy ping-pong
```
kubectl apply -f ping-pong/manifests
```

## Check status
```
kubectl get statefulset -n exercises
kubectl get pods -n exercises
kubectl get pvc -n exercises
kubectl get pv
```

## Debug the database directly (optional)
A disposable pod with the psql client, deleted automatically on exit:
```
kubectl run -it --rm --restart=Never --image postgres -n exercises psql-for-debugging -- sh
```
Inside it:
```
psql postgres://pingpong:pingpongpass@postgres-svc.exercises.svc.cluster.local:5432/pingpong
\dt
SELECT * FROM counter;
```

## View postgres logs
```
kubectl logs postgres-stset-0 -n exercises
```

## Test
Only one Ingress can serve path / at a time, disable Todo app's
if it is currently active:
```
kubectl delete ingress todo-app-ingress -n project
```
```
curl http://localhost:8081/pingpong
curl http://localhost:8081/pingpong
curl http://localhost:8081/
```

## Confirm the counter survives a pod restart
```
kubectl delete pod -l app=ping-pong -n exercises
curl http://localhost:8081/
```
The count should keep its previous value, not reset to 0.

## Confirm StatefulSet identity and data survive a postgres restart
```
kubectl delete pod postgres-stset-0 -n exercises
kubectl get pods -n exercises -l app=postgres
```
The replacement pod should have the exact same name
(postgres-stset-0), and:
```
curl http://localhost:8081/
```
The count should still be intact.

## Access
Cluster must be created with:
```
k3d cluster create --port 8082:30080@agent:0 -p 8081:80@loadbalancer --agents 2
```