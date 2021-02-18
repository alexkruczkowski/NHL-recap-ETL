from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago

import nhl_etl
from nhl_etl import run_nhl_etl

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(0,0,0,0,0),
    'email': ['ak.kruczkowski@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

dag = DAG(
    'nhl_dag',
    default_args=default_args,
    description='Testing dags for the first time',
    schedule_interval=timedelta(days=1),
)

def just_a_function():
    print("Testing output)")

run_etl = PythonOperator(
    task_id='nhl-etl',
    python_callable=run_nhl_etl,
    dag=dag,
)

run_etl
