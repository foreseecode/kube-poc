Install Prometheus :

```helm install prometheus stable/prometheus --namespace monitoring```

Install Grafana :

```kubectl apply -f config.yml```

```helm install grafana stable/grafana -f values.yml --namespace monitoring```

To get password :

```kubectl get secret -n monitoring grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo```


Port Forward :

```kubectl -n monitoring port-forward <grafana-pod-name> 3000:3000```

