# Todo app

Web server for the course project. Responds to GET / with an hourly-cached image (see note on caching below), and GET /image with the raw image data. Port is configurable via the PORT environment variable.

## Image caching
A random image is fetched from Lorem Picsum (https://picsum.photos/1200) and cached to a PersistentVolume so it survives pod restarts and container crashes. The image stays the same for 10 minutes; after that, the next request fetches a new one.

Note: the exercise text says "hourly image" in the heading but specifies "10 minutes" in the instructions. This implementation follows the explicit 10 minute requirement.

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
docker build -t todo-app:latest ./todo-app
k3d image import todo-app:latest -c k3s-default
kubectl apply -f persistent-volume
kubectl apply -f todo-app/manifests
```

## Required one-time setup
The PersistentVolume uses a local path on the k3d agent node, create it before applying the manifests:

```
docker exec k3d-k3s-default-agent-0 mkdir -p /tmp/kube-todo
```

## Check status
```
kubectl get pv,pvc
kubectl get pods
```

## Test caching
```
curl http://localhost:8081/image -o img1.jpg
curl http://localhost:8081/image -o img2.jpg
diff img1.jpg img2.jpg   # should be identical within 10 minutes
```

## Test persistence across restarts
```
kubectl delete pod -l app=todo-app
curl http://localhost:8081/image -o img3.jpg
diff img1.jpg img3.jpg   # should still be identical, image survives the restart
```

## Access
Cluster must be created with:
```
k3d cluster create --port 8082:30080@agent:0 -p 8081:80@loadbalancer --agents 2
```

Then open http://localhost:8081

Note: if "Log output" Ingress is also applied, delete it first to avoid routing conflicts, since both currently use path /.

```
kubectl delete ingress log-output-ingress
```