# 3.5 - The project, with Kustomize

"The project" (todo-app, todo-backend, postgres, wikipedia-reminder)
deployed to GKE, now managed with Kustomize instead of individual
`kubectl apply -f` commands. Namespace: `project`.

## Build (with the final Docker Hub tags, before any local test)

```
docker build -t diegoespinozapacheco/todo-app-gke:latest ./todo-app
docker build -t diegoespinozapacheco/todo-backend-gke:latest ./todo-backend
docker build -t diegoespinozapacheco/wikipedia-reminder-gke:latest ./wikipedia-reminder
```

## Push to Docker Hub

```
docker login
docker push diegoespinozapacheco/todo-app-gke:latest
docker push diegoespinozapacheco/todo-backend-gke:latest
docker push diegoespinozapacheco/wikipedia-reminder-gke:latest
```

## Local check (k3d-k3s-default, namespace project)

Kustomize rewrites the image names to the Docker Hub tags above, so
k3d pulls the real images (no `imagePullPolicy: Never`).

```
kubectx k3d-k3s-default
kubectl apply -k .
```

```
kubectl rollout status statefulset/postgres-stset -n project
kubectl rollout status deployment/todo-backend -n project
kubectl rollout status deployment/todo-app -n project
```

```
kubectl port-forward --address 0.0.0.0 -n project svc/todo-backend-svc 3013:2348
kubectl port-forward --address 0.0.0.0 -n project svc/todo-app-svc 3012:2345
```

```
curl http://localhost:3013/            # 200, health check
curl http://localhost:3013/todos       # []
curl -X POST http://localhost:3013/todos -H "Content-Type: application/json" -d '{"content":"test"}'
curl http://localhost:3013/todos       # [{"content":"test"}]
curl http://localhost:3012/            # frontend HTML
```

Note: locally `/` and `/todos` are on separate ports (no Gateway
installed in k3d), so the frontend's own `fetch('/todos')` fails when
opened in a browser against port 3012 - that's expected. The
Gateway/HTTPRoute below is only applied on GKE.

Trigger the reminder manually instead of waiting for the hourly
schedule:

```
kubectl create job --from=cronjob/wikipedia-reminder wikipedia-reminder-manual-1 -n project
kubectl logs -n project -l job-name=wikipedia-reminder-manual-1
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
kubectl apply -k .
kubectl apply -f todo-app/manifests/gateway.yaml -f todo-app/manifests/route.yaml
```

```
kubectl rollout status statefulset/postgres-stset -n project
kubectl rollout status deployment/todo-backend -n project
kubectl rollout status deployment/todo-app -n project
```

## Verify

```
kubectl get gateway my-gateway -n project --watch
```

Wait for `PROGRAMMED: True` and an `ADDRESS`. Then:

```
curl http://<ADDRESS>/
curl http://<ADDRESS>/todos
curl -X POST http://<ADDRESS>/todos -H "Content-Type: application/json" -d '{"content":"from GKE"}'
curl http://<ADDRESS>/todos
```

Open `http://<ADDRESS>/` in a browser: the frontend loads the todo
list on its own, since `/` and `/todos` are on the same origin behind
the Gateway.

Trigger the reminder manually to confirm it also works on GKE:

```
kubectl create job --from=cronjob/wikipedia-reminder wikipedia-reminder-manual-1 -n project
kubectl logs -n project -l job-name=wikipedia-reminder-manual-1
```

## Shut down (billing stops here)

```
gcloud container clusters delete dwk-cluster --zone=europe-north1-b
kubectx local
```