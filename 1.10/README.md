# Log output (multi-container)

Split into two containers sharing a pod via an emptyDir volume:

- log-randomizer: generates a random string on startup and
  appends a line with the string and a timestamp to a shared
  file every 5 seconds.
- http-endpoint: reads that shared file and serves its content
  on GET /.

Data is lost if the pod restarts, since it lives in an emptyDir
volume.

## Workdir

Please use 1.10 as your main directory when executing this Readme commands

## Build and import images
```
docker build -t log-randomizer:latest ./log-randomizer
docker build -t http-endpoint:latest ./http-endpoint
k3d image import log-randomizer:latest http-endpoint:latest -c k3s-default
```

## Remove old deployment
```
kubectl delete deployment log-output
```

## Deploy 1.10 version
```
kubectl apply -f manifests
```

## Check status
```
kubectl get pods
```

## Inspect the shared file directly (optional)
```
kubectl exec <pod-name> -c log-randomizer -- cat /usr/src/app/files/log.txt
```

## Access
Cluster must be created with:
```
k3d cluster create --port 8082:30080@agent:0 -p 8081:80@loadbalancer --agents 2
```

Then open http://localhost:8081