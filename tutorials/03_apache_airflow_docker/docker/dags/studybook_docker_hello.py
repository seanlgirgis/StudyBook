"""
Sample DAG for StudyBook Docker Airflow stack.
"""

from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator


def _hello() -> None:
    print("Hello from Airflow running in Docker")


with DAG(
    dag_id="studybook_docker_hello",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=["studybook", "docker", "airflow"],
) as dag:
    PythonOperator(
        task_id="say_hello",
        python_callable=_hello,
    )