# 3.3 - To the Gateway

"Log output" and "Ping-pong" deployed to GKE, now exposed through
the Gateway API (`Gateway` + `HTTPRoute`) instead of an Ingress.
Same namespace (`gcp-gke`), same apps and images as `3.2` - only
the routing layer and the Service type change.

## Build (only needed if app code changed since 3.2)

```
docker build -t diegoespinozapacheco/log-randomizer-gke:latest ./log-output/log-randomizer
docker build -t diegoespinozapacheco/http-endpoint-gke:latest ./log-output/http-endpoint
docker build -t diegoespinozapacheco/ping-pong-gke:latest ./ping-pong
```

## Push to Docker Hub

```
docker login
docker push diegoespinozapacheco/log-randomizer-gke:latest
docker push diegoespinozapacheco/http-endpoint-gke:latest
docker push diegoespinozapacheco/ping-pong-gke:latest
```

## Local check (k3d-k3s-default, same gcp-gke namespace)

The Gateway API controller itself is GKE-managed and cannot be
tested in k3d, so only the app logic is validated here, through
each Service's own port-forward:

```
kubectx k3d-k3s-default
kubectl apply -f namespaces
kubectl apply -f ping-pong/manifests/deployment.yaml -f ping-pong/manifests/service.yaml
kubectl apply -f log-output/manifests/deployment.yaml -f log-output/manifests/service.yaml
kubectl port-forward --address 0.0.0.0 -n gcp-gke svc/ping-pong-svc 3010:80
kubectl port-forward --address 0.0.0.0 -n gcp-gke svc/log-output-svc 3011:80
```

```
curl http://localhost:3010/          # should return "ok" (health check)
curl http://localhost:3010/pingpong
curl http://localhost:3011/          # timestamp + "Ping / Pongs: N"
```

## Create the GKE cluster and enable Gateway API

Billing starts here.

```
gcloud container clusters create dwk-cluster \
  --zone=europe-north1-b \
  --cluster-version=1.36 \
  --disk-size=32 \
  --num-nodes=4 \
  --machine-type=e2-small

gcloud container clusters update dwk-cluster --location=europe-north1-b --gateway-api=standard
```

```
kubectx
```

Rename the new context, e.g.:

```
kubectx gke=<generated-context-name>
kubectx gke
```

## Deploy

Namespace and apps first, Gateway and Route last:

```
kubectl apply -f namespaces
kubectl apply -f ping-pong/manifests/deployment.yaml -f ping-pong/manifests/service.yaml
kubectl apply -f log-output/manifests/deployment.yaml -f log-output/manifests/service.yaml
kubectl apply -f log-output/manifests/gateway.yaml
kubectl apply -f log-output/manifests/route.yaml
```

## Verify

```
kubectl get gateway my-gateway -n gcp-gke --watch
```

Wait for `PROGRAMMED: True` and an `ADDRESS`. This takes noticeably
longer than an Ingress, especially the first time Gateway API is
enabled on a cluster.

```
curl http://<ADDRESS>/
curl http://<ADDRESS>/pingpong
curl http://<ADDRESS>/pingpong
curl http://<ADDRESS>/
```

Note: the Ping-pong counter is in-memory and does not persist; it
resets to 0 if the pod restarts or the cluster is deleted.

## Shut down (billing stops here)

```
gcloud container clusters delete dwk-cluster --zone=europe-north1-b
kubectx local
```