from __future__ import annotations
from airflow import DAG
from datetime import datetime, timedelta
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python import PythonOperator
import kubernetes
from kubernetes import client,watch
from kubernetes.client.rest import ApiException
from pprint import pprint

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(year=2022, month=5, day=23)
}

test_labels = {
    'app.foresee/application':'hello-world',
    'test' : 'label'
}

annotations = {
    'app.foresee/application':'hello-world'
}

service_manifest = {
    "kind": "Service",
    "apiVersion": "v1",
    "metadata": {
        "app.foresee/application": "hello-world"
    },
    "spec": {
        "selector": {
            "app.foresee/application": "hello-world"
        },
        "ports": [
            {
                "protocol": "TCP",
                "port": 5000,
                "targetPort": 5000
            }
        ]
    }
}

namespace = 'airflow'


def create_configMap():
    api_instance = kubernetes.client.CoreV1Api()
    cmap = client.V1ConfigMap()
    cmap.metadata = client.V1ObjectMeta(name="special-config")
    cmap.data = {}
    cmap.data["special.how"] = "very"
    cmap.data["special.type"] = "charm"

    try:
        api_response = api_instance.create_namespaced_config_map(namespace, body=cmap)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling CoreV1Api->create_namespaced_config_map: %s\n" % e)

def create_service():
    api_instance = kubernetes.client.CoreV1Api()

    try:
        api_response = api_instance.create_namespaced_service(namespace, service_manifest, pretty='true')
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling CoreV1Api->create_namespaced_endpoints: %s\n" % e)

dag = DAG(
    'hello-world-spin-up', default_args=default_args, schedule_interval='@daily')

start = DummyOperator(task_id='run_this_first', dag=dag)

spin_up_image = KubernetesPodOperator(
        namespace='airflow',
        image='digitalocean/flask-helloworld',
        name="spin_up_image",
        do_xcom_push=False,
        is_delete_operator_pod=False,
        in_cluster=True,
        task_id="spin_up_image",
        get_logs=True,
        labels=test_labels,
        annotations=annotations,
        dag=dag
    )

create_service = PythonOperator(
        task_id='create_service',
        python_callable=create_service,
        dag=dag
    )

create_configMap = PythonOperator(
        task_id='create_configMap',
        python_callable=create_configMap,
        dag=dag
    )

start >> create_configMap
