# Monitoring stack

Observability stack installed via Helm: Prometheus (metrics),
Loki (log storage), Alloy/k8s-monitoring (log collection from
every node), and Grafana (UI for both). Simplified for local lab
use: single instances, no alerting, local filesystem storage,
no persistence guarantees across pod restarts.

## How to consume
Not an app you call directly. Access the UI:
```
kubectl port-forward --address 0.0.0.0 --namespace monitoring svc/grafana 3000:80
```
Then open http://localhost:3000 (admin / admin) and use Explore
with either the Prometheus or Loki datasource.

Example PromQL query (pod count by namespace):
```
count by (namespace) (kube_pod_info)
```

Example LogQL query (todo-backend rejected requests):
```
{namespace="project"} |= "REJECTED"
```