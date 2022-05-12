import logging
from boto3.session import Session
import botocore
import os
import yaml
from pathlib import Path
from airflow.models import DAG
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from datetime import datetime


default_args = {
    'start_date': datetime(year=2022, month=5, day=10)
}



def generate_kubeconfig():
    ACCESS_KEY = Variable.get("k8s_test_aws_access_key")
    SECRET_KEY = Variable.get("k8s_test_aws_secret_key")
    home_path = str(Path.home())
    region = "us-east-1"
    
    kube_path = home_path + "/.kube/"

    folder_path = Path(kube_path) #define folder structure
    if not os.path.exists(kube_path):   # create folders if not exists
         os.makedirs(kube_path)

    file_path = os.path.join(kube_path, 'config')  # add file to the folder path
    f = open(file_path,"w+") 
    print(file_path)

    s = Session(aws_access_key_id=ACCESS_KEY,
                aws_secret_access_key=SECRET_KEY,
                region_name="us-east-1")
    eks = s.client("eks")

    # get cluster details
    cluster_name = "xm-scp-poc"
    cluster = eks.describe_cluster(name=cluster_name)
    cluster_cert = cluster["cluster"]["certificateAuthority"]["data"]
    cluster_ep = cluster["cluster"]["endpoint"]

    # build the cluster config hash
    cluster_config = {
            "apiVersion": "v1",
            "kind": "Config",
            "clusters": [
                {
                    "cluster": {
                        "server": str(cluster_ep),
                        "certificate-authority-data": str(cluster_cert)
                    },
                    "name": "kubernetes"
                }
            ],
            "contexts": [
                {
                    "context": {
                        "cluster": "kubernetes",
                        "user": "aws"
                    },
                    "name": "aws"
                }
            ],
            "current-context": "aws",
            "preferences": {},
            "users": [
                {
                    "name": "aws",
                    "user": {
                        "exec": {
                            "apiVersion": "client.authentication.k8s.io/v1alpha1",
                            "command": "aws",
                            "args": [
                                 "eks", "get-token",
                                "--region", region,
                                "--cluster-name", cluster_name
                            ]
                        }
                    }
                }
            ]
        }

    print(cluster_config)

with DAG(
    dag_id='pratik_generate_kubeconfig',
    default_args = default_args,
    schedule_interval='@daily',
    description='Generate Kubeconfigs'
) as dag:

    # Task 1 - Fetch user data from the API
    generate_kubeconfig = PythonOperator(
        task_id='generate_kubeconfig',
        python_callable=generate_kubeconfig,
        op_kwargs={}
    )

    generate_kubeconfig
