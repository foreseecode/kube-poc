# Logging with EFK in Kubernetes

$ helm install elasticsearch stable/elasticsearch 
wait for few minutes..

$ kubectl create -f fluentd-rbac.yaml

$ kubectl create -f fluentd-daemonset.yaml

$ helm install kibana stable/kibana -f kibana-values.yaml

Open Kibana dashboard.