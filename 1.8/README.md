# Todo app
 
Web server that responds to GET / and prints "Server started in port X" on startup. Port is configurable via the PORT
environment variable.
 
## Run locally
```
PORT=3000 python main.py
```
 
## Run in Docker
```
docker build -t todo-app .
docker run -e PORT=3000 -p 3000:3000 todo-app
```
 
## Deploy to k3d
```
docker build -t todo-app:latest .
k3d image import todo-app:latest
kubectl apply -f manifests
``` 

## Access
Cluster must be created with:

```
k3d cluster create --port 8082:30080@agent:0 -p 8081:80@loadbalancer --agents 2
```
 
Then open http://localhost:8081

## Note
If "Log output" Ingress is also applied, delete it first
to avoid routing conflicts, since both currently use path /.

```
kubectl delete ingress log-output-ingress
```