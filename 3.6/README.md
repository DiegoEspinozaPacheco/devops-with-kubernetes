# 3.6 - The project, with CI/CD

"The project" (todo-app, todo-backend, postgres, wikipedia-reminder),
same as 3.5, but build/push/deploy is now automated with GitHub
Actions instead of manual commands. A push that touches anything
under `3.6/` builds the three app images, pushes them to Google
Artifact Registry, and deploys with Kustomize - see
`.github/workflows/project-deploy.yaml` at the repo root.

## One-time GCP setup (already done for this repo, kept here for reference)

Artifact Registry repository:
```
gcloud artifacts repositories create dwk-project \
  --repository-format=docker \
  --location=europe-north1
```

Service account used by the pipeline, with just enough permissions to
push images and manage the GKE cluster:
```
gcloud iam service-accounts create "github-actions-sa" \
  --display-name="GitHub Actions SA"

gcloud projects add-iam-policy-binding dwk-gke-dep \
  --role="roles/artifactregistry.writer" \
  --member="serviceAccount:github-actions-sa@dwk-gke-dep.iam.gserviceaccount.com"

gcloud projects add-iam-policy-binding dwk-gke-dep \
  --role="roles/container.admin" \
  --member="serviceAccount:github-actions-sa@dwk-gke-dep.iam.gserviceaccount.com"
```

Workload Identity Federation, so GitHub Actions can authenticate to
GCP without storing any credentials as secrets:
```
gcloud iam workload-identity-pools create "github-pool" \
  --location="global" \
  --display-name="GitHub Actions Pool"

gcloud iam workload-identity-pools providers create-oidc "github-provider" \
  --location="global" \
  --workload-identity-pool="github-pool" \
  --display-name="GitHub provider" \
  --attribute-mapping="google.subject=assertion.sub,attribute.repository=assertion.repository" \
  --attribute-condition="assertion.repository=='DiegoEspinozaPacheco/devops-with-kubernetes'" \
  --issuer-uri="https://token.actions.githubusercontent.com"

gcloud iam service-accounts add-iam-policy-binding \
  github-actions-sa@dwk-gke-dep.iam.gserviceaccount.com \
  --role="roles/iam.workloadIdentityUser" \
  --member="principalSet://iam.googleapis.com/projects/428339135151/locations/global/workloadIdentityPools/github-pool/attribute.repository/DiegoEspinozaPacheco/devops-with-kubernetes"
```

GitHub Environment `GKE_PROJECT`, holding 3 secrets: `GKE_PROJECT`
(the GCP project ID), `SERVICE_ACCOUNT`
(`github-actions-sa@dwk-gke-dep.iam.gserviceaccount.com`), and
`WORKLOAD_IDENTITY_PROVIDER`
(`projects/428339135151/locations/global/workloadIdentityPools/github-pool/providers/github-provider`).

## What the pipeline does (`.github/workflows/project-deploy.yaml`)

On every push that touches `3.6/**`:

1. Authenticates to GCP via Workload Identity Federation (no stored
   credentials)
2. Builds `todo-app`, `todo-backend` and `wikipedia-reminder`,
   tagged `<registry>/<project>/<repository>/<image>:main-<commit-sha>`
3. Pushes all three to Artifact Registry
4. `kustomize edit set image` for each, then
   `kustomize build . | kubectl apply -f -`
5. Waits for `todo-app` and `todo-backend` rollouts to complete

`todo-app`'s Deployment uses `strategy: Recreate` instead of the
default `RollingUpdate`: its PVC is `ReadWriteOnce`, so a rolling
update would try to mount the same volume from two pods at once and
hang. `Recreate` terminates the old pod before starting the new one.

## What is still manual (not covered by the pipeline)

The pipeline only manages what is inside `3.6/kustomization.yaml`.
These are applied once, outside the pipeline:

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
kubectl apply -f namespaces/project.yaml
kubectl apply -f todo-app/manifests/gateway.yaml -f todo-app/manifests/route.yaml
```

## Verify

```
kubectl get gateway my-gateway -n project
```

```
curl http://<ADDRESS>/
curl http://<ADDRESS>/todos
```

## Shut down (billing stops here)

```
gcloud container clusters delete dwk-cluster --zone=europe-north1-b
kubectx local
```

Deleting the cluster does not affect the pipeline itself or the
images in Artifact Registry - recreating the cluster and re-running
the workflow (or pushing a commit) redeploys everything.