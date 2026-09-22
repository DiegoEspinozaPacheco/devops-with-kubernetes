# 3.2 - Back to Ingress

"Log output" and "Ping-pong" deployed to GKE, exposed through a
single Ingress (namespace `gcp-gke`) instead of one LoadBalancer
per app. Ping-pong responds on `/pingpong`; each backend's root
path `/` must return 200, since GKE's Ingress health-checks every
backend there regardless of which path it's actually mapped to.

## Build (with the final Docker Hub tag from the start)

```
docker build -t diegoespinozapacheco/log-randomizer-gke:latest ./log-output/log-randomizer
docker build -t diegoespinozapacheco/http-endpoint-gke:latest ./log-output/http-endpoint
docker build -t diegoespinozapacheco/ping-pong-gke:latest ./ping-pong
```

## Push to Docker Hub (before testing against any cluster)

```
docker login
docker push diegoespinozapacheco/log-randomizer-gke:latest
docker push diegoespinozapacheco/http-endpoint-gke:latest
docker push diegoespinozapacheco/ping-pong-gke:latest
```

## Local check (k3d-k3s-default, same gcp-gke namespace)

Validates app logic. GKE's real Ingress (GCE) cannot be tested
here, so each Service is checked with its own port-forward:

```
kubectx k3d-k3s-default
kubectl apply -f namespaces
kubectl apply -f ping-pong/manifests
kubectl apply -f log-output/manifests
kubectl port-forward --address 0.0.0.0 -n gcp-gke svc/ping-pong-svc 3010:80
kubectl port-forward --address 0.0.0.0 -n gcp-gke svc/log-output-svc 3011:80
```

```
curl http://localhost:3010/          # should return "ok" (health check)
curl http://localhost:3010/pingpong
curl http://localhost:3011/          # timestamp + "Ping / Pongs: N"
```

## Create the GKE cluster

Billing starts here.

```
gcloud container clusters create dwk-cluster \
  --zone=europe-north1-b \
  --cluster-version=1.36 \
  --disk-size=32 \
  --num-nodes=4 \
  --machine-type=e2-small
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
kubectl apply -f ping-pong/manifests
kubectl apply -f log-output/manifests
```

## Verify

```
kubectl get pods -n gcp-gke
kubectl get ing -n gcp-gke --watch
```

While the Google load balancer propagates, `404`/`502` responses
are expected (GCLB's default page, not the app's). Wait for the
backend to turn `HEALTHY` (`kubectl describe ingress -n gcp-gke`
if it takes a while).

Once the `ADDRESS` is available:

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
kubectx gke
gcloud container clusters delete dwk-cluster --zone=europe-north1-b
kubectx local
```