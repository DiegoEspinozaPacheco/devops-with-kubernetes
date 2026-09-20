# 3.1 - Pingpong GKE

Ping-pong deployed to Google Kubernetes Engine, exposed with a
LoadBalancer Service instead of an Ingress. Namespace `gcp-gke` is
used for this and all future cloud (GCP/GKE) exercises, separate
from the local k3d namespaces (`exercises`, `project`).

## Local pre-check (optional, before spending GCP credits)

Uses the existing local `k3d-k3s-default` cluster, same namespace.
The Service stays in `<pending>` forever locally, since k3d has no
LoadBalancer provider; use port-forward to verify the app itself.

```
kubectx k3d-k3s-default
docker build -t ping-pong-gke:latest ./ping-pong
k3d image import ping-pong-gke:latest -c k3s-default
kubectl apply -f namespaces
kubectl apply -f ping-pong/manifests
kubectl port-forward --address 0.0.0.0 -n gcp-gke svc/ping-pong-svc 3003:80
```

```
curl http://localhost:3003/pingpong
```

## Push image to Docker Hub

GKE cannot use a locally-cached image like k3d can, so it must be
pulled from a registry.

```
docker tag ping-pong-gke:latest <dockerhub-user>/ping-pong-gke:latest
docker login
docker push <dockerhub-user>/ping-pong-gke:latest
```

Update `manifests/deployment.yaml`'s `image` field to match, and
remove `imagePullPolicy: Never` (that flag is only needed for the
local k3d test above).

## Set up the GCP project (one time)

```
gcloud config set project dwk-gke-dep
gcloud billing projects describe dwk-gke-dep
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

Rename the new context for clarity, e.g.:

```
kubectx gke=<generated-context-name>
kubectx gke
```

## Deploy

```
kubectl apply -f namespaces
kubectl apply -f ping-pong/manifests
```

## Verify

```
kubectl get pods -n gcp-gke
kubectl get svc -n gcp-gke --watch
```

Wait for `EXTERNAL-IP` to leave `<pending>`, then:

```
curl http://<EXTERNAL-IP>/pingpong
```

Note: the LoadBalancer only exposes port 80 (HTTP); HTTPS is not
available.

## Shut down (billing stops here)

Deleting the cluster removes everything deployed on it. Since the
manifests are declarative, resuming later only requires re-applying
them once a new cluster exists.

```
kubectx gke
gcloud container clusters delete dwk-cluster --zone=europe-north1-b
kubectx local
```