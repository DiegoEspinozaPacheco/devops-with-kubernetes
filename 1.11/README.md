# The Project (app convergence)

This project has joined log output app that has 2 containers and ping pong app that basically generates a counter based on how many get requests are done.

Both apps have a bit more of information with their own Readmes.

Data is preserved due PV utilization.

## Workdir

Please use 1.11 as your main directory when executing this Readme commands

## Build and import images
```
docker build -t log-randomizer:latest ./log-output/log-randomizer
docker build -t http-endpoint:latest ./log-output/http-endpoint
docker build -t ping-pong:latest ./ping-pong
k3d image import log-randomizer:latest http-endpoint:latest ping-pong:latest -c k3s-default
```

## Remove old deployment
```
kubectl delete deployment log-output
kubectl delete deployment ping-pong
```

## Deploy 1.11 version of The Project
```
kubectl apply -f ./log-output/manifests -f ./ping-pong/manifests
```

## Check status
```
kubectl get pods
kubectl get deployments
```

## Access
Cluster must be created with:
```
k3d cluster create --port 8082:30080@agent:0 -p 8081:80@loadbalancer --agents 2
```

Then open http://localhost:8081 to check the random UUID with its most recent timestamp and to check the Pingpong counter

If you want to increase the pingpong counter, check http://localhost:8081/pingpong