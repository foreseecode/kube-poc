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

test_lables = {
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
                "port": 8080,
                "targetPort": 8080
            }
        ]
    }
}

def create_service():
    api_instance = kubernetes.client.CoreV1Api()
    service_ns = 'airflow'

    try:
        api_response = api_instance.create_namespaced_service(service_ns, service_manifest, pretty='true')
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling CoreV1Api->create_namespaced_endpoints: %s\n" % e)

dag = DAG(
    'hello-world-spin-up', default_args=default_args, schedule_interval='@daily')

start = DummyOperator(task_id='run_this_first', dag=dag)

spin_up_image = KubernetesPodOperator(
        namespace='airflow',
        image='fsr-artifactory.aws.foreseeresults.com:9001/hello-world-service:snapshot-210921-192304-0177',
        name="spin_up_image",
        do_xcom_push=True,
        is_delete_operator_pod=False,
        in_cluster=True,
        task_id="spin_up_image",
        get_logs=True,
        labels=test_lables,
        annotations=annotations,
        dag=dag
    )

create_service = PythonOperator(
        task_id='create_service',
        python_callable=create_service,
        dag=dag
    )

start >> spin_up_image >> create_service
