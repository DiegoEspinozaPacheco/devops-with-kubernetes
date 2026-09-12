# 2.10 - The project, step 13

The project now has request logging: every GET and POST to
todo-backend is logged, and rejected todos (over 140 characters,
empty, or malformed) are logged as REJECTED. A monitoring stack
(Prometheus, Loki, Alloy, Grafana) installed via Helm lets you
view those logs and cluster metrics.

## Check current context and namespace
```
kubectx
kubens
```

## Install Helm (if not already installed)
```
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```

## Add repos and create the monitoring namespace
```
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
kubectl create namespace monitoring
```

## Install the monitoring stack, in dependency order
```
helm upgrade --install prom prometheus-community/prometheus \
  --namespace monitoring \
  --values monitoring/prom-values.yaml

helm upgrade --install loki grafana/loki \
  --namespace monitoring \
  --values monitoring/loki-values.yaml

helm upgrade --install k8smon grafana/k8s-monitoring \
  --namespace monitoring \
  --values monitoring/k8smon-values.yaml

helm upgrade --install grafana grafana/grafana \
  --namespace monitoring \
  --values monitoring/grafana-values.yaml
```

## Check status
```
helm list --namespace monitoring
kubectl get pods --namespace monitoring
```
Wait until all four releases (prom, loki, k8smon, grafana) show
pods in Running state.

## Build and import todo-backend image
```
docker build -t todo-backend:latest ./todo-backend
k3d image import todo-backend:latest -c k3s-default
kubectl rollout restart deployment/todo-backend -n project
```

## Access Grafana
```
kubectl port-forward --address 0.0.0.0 --namespace monitoring svc/grafana 3000:80
```
Open http://localhost:3000 (or http://<host-ip>:3000 from another
device), login admin / admin.

## Generate test traffic, including rejected todos
Only one Ingress can serve path / at a time, disable Log
output's if it is currently active:
```
kubectl delete ingress log-output-ingress -n exercises
```
```
curl -X POST http://localhost:8081/todos -H "Content-type: application/json" -d '{"content":"Todo normal"}'
curl -X POST http://localhost:8081/todos -H "Content-type: application/json" -d "{\"content\":\"$(python3 -c 'print("x"*150)')\"}"
curl -X POST http://localhost:8081/todos -H "Content-type: application/json" -d '{"content":""}'
```

## View the rejected todos in Grafana
In Explore, select the Loki datasource, code mode, and run:
```
{namespace="project"} |= "REJECTED"
```

## If resources are tight on the host
The full monitoring stack is heavy for a small local machine. If
pods stay Pending or a component keeps restarting, either lower
memory pressure by disabling the chunks cache:
```
kubectl scale statefulset loki-chunks-cache -n monitoring --replicas=0
```
or uninstall the stack entirely when not actively using it:
```
helm uninstall grafana --namespace monitoring
helm uninstall k8smon --namespace monitoring
helm uninstall loki --namespace monitoring
helm uninstall prom --namespace monitoring
```
Reinstall later with the same helm upgrade --install commands above.

## Access
Cluster must be created with:
```
k3d cluster create --port 8082:30080@agent:0 -p 8081:80@loadbalancer --agents 2
```