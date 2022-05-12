from airflow.models import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import (
    KubernetesPodOperator,
)

default_args = {
    'start_date': datetime(year=2022, month=5, day=10)
}


with DAG(
    dag_id='k8s_dry_run',
    default_args = default_args,
    schedule_interval='@daily',
    description='K8s dry run'
) as dag:

    # Task 1 - Fetch user data from the API
    k = KubernetesPodOperator(
        name="hello-dry-run",
        image="debian",
        cmds=["bash", "-cx"],
        arguments=["echo", "10"],
        labels={"foo": "bar"},
        task_id="dry_run_demo",
        do_xcom_push=True,
    )

    k.dry_run()