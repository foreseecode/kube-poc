# Logging with EFK in Kubernetes

$ helm install elasticsearch stable/elasticsearch 
wait for few minutes..

$ kubectl create -f fluentd-rbac.yaml

$ kubectl create -f fluentd-daemonset.yaml

$ helm install kibana stable/kibana -f kibana-values.yaml

For elasticsearch - 

export POD_NAME=$(kubectl get pods --namespace default -l "app=elasticsearch,component=client,release=elasticsearch" -o jsonpath="{.items[0].metadata.name}")

echo "Visit http://127.0.0.1:9200 to use Elasticsearch"

kubectl port-forward --namespace default $POD_NAME 9200:9200

For kibana - 

export POD_NAME=$(kubectl get pods --namespace default -l "app=kibana,release=kibana" -o jsonpath="{.items[0].metadata.name}")

echo "Visit http://127.0.0.1:5601 to use Kibana"

kubectl port-forward --namespace default $POD_NAME 5601:5601
