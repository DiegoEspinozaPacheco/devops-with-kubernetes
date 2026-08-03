## Log output + ping-pong apps
 
Build and import images:
```
docker build -t log-output:latest ./log-output
docker build -t ping-pong:latest ./ping-pong
k3d image import log-output:latest ping-pong:latest -c k3s-default
```
 
Clean up old deployments:
```
kubectl delete deployment log-output ping-pong todo-app --ignore-not-found
kubectl delete ingress todo-app-ingress --ignore-not-found
```
 
Apply manifests:
```
kubectl apply -f log-output/manifests
kubectl apply -f ping-pong/manifests
```
 
Check status:
```
kubectl get pods
kubectl get svc,ing
kubectl describe ingress log-output-ingress
```
 
Test endpoints:
```
curl http://localhost:8081/
curl http://localhost:8081/pingpong
```
 
Follow logs:
```
kubectl logs -f deployment/log-output
```