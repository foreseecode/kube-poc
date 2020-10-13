Elasticsearch - 

```export POD_NAME=$(kubectl get pods --namespace default -l "app=elasticsearch,component=client,release=elasticsearch" -o jsonpath="{.items[0].metadata.name}")```

```kubectl port-forward --namespace default $POD_NAME 9200:9200```

Kibana - 

```export POD_NAME=$(kubectl get pods --namespace default -l "app=kibana,release=kibana" -o jsonpath="{.items[0].metadata.name}")```

```kubectl port-forward --namespace default $POD_NAME 5601:5601```

Prometheus - 

```kubectl --namespace monitoring port-forward svc/prometheus-k8s 9090```

Grafana - 

```kubectl --namespace monitoring port-forward svc/grafana 3000```

Alertmanager - 

```kubectl --namespace monitoring port-forward svc/alertmanager-main 9093```
