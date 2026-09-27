# 3.4 - Rewritten routing

"Log output" and "Ping-pong" deployed to GKE, same as `3.3`, but
Ping-pong no longer needs to know about cluster-level URL structure.
It responds on `/` instead of `/pingpong`; the `HTTPRoute` rewrites
external `/pingpong` requests to `/` before forwarding them to the
pod.

## Build (with the final Docker Hub tag, before any local test)

```
docker build -t diegoespinozapacheco/ping-pong-gke:latest ./ping-pong
```
(`log-randomizer` and `http-endpoint` are unchanged from `3.3` -
no rebuild needed unless their code changed.)

## Push to Docker Hub

```
docker login
docker push diegoespinozapacheco/ping-pong-gke:latest
```

## Local check (k3d-k3s-default, same gcp-gke namespace)

```
kubectx k3d-k3s-default
kubectl apply -f namespaces
kubectl apply -f ping-pong/manifests/deployment.yaml -f ping-pong/manifests/service.yaml
kubectl apply -f log-output/manifests/deployment.yaml -f log-output/manifests/service.yaml
kubectl rollout restart deployment/ping-pong -n gcp-gke
kubectl rollout status deployment/ping-pong -n gcp-gke
```

```
kubectl port-forward --address 0.0.0.0 -n gcp-gke svc/ping-pong-svc 3010:80
kubectl port-forward --address 0.0.0.0 -n gcp-gke svc/log-output-svc 3011:80
```

```
curl http://localhost:3010/          # "pong N" - real logic now lives here
curl http://localhost:3010/pingpong  # 404 - the app no longer knows this path
curl http://localhost:3011/
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

Wait for `PROGRAMMED: True` and an `ADDRESS`. Then:

```
curl http://<ADDRESS>/
curl http://<ADDRESS>/pingpong
curl http://<ADDRESS>/pingpong
```

`/pingpong` should behave exactly like `/` (same counter, same
increment) - that confirms the route rewrite is working.

Note: the health check GCLB runs against `/` also increments the
counter now, since `/` is the app's real logic in this exercise -
the counter climbing on its own without manual requests is expected.

## Shut down (billing stops here)

```
gcloud container clusters delete dwk-cluster --zone=europe-north1-b
kubectx local
```