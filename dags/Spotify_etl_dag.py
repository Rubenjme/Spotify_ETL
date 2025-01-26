#-------------------------------------------------------------------------------------------------
# Este archivo contiene el código para programar el DAG que ejecutará el pipeline ETL diariamente.
#-------------------------------------------------------------------------------------------------
from airflow import DAG                                # Importa la clase DAG
from airflow.operators.python import PythonOperator    # Importa el operador Python de Airflow 
from datetime import datetime, timedelta
from ETL_Pipeline import etl_pipeline                  # Importa la función ETL combinada

# Argumentos por defecto para el DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Defino el DAG
dag = DAG(
    'Spotify_etl_dag',                    # Nombre del DAG que aparecerá en Airflow
    default_args=default_args,
    description='Spotify ETL Pipeline',
    schedule_interval=timedelta(days=1),  # Se ejecuta diariamente
    start_date=datetime(2025, 1, 1),      # Fecha de inicio del DAG
    catchup=False,
)

# Define la tarea que ejecuta el pipeline ETL
etl_task = PythonOperator(
    task_id='run_spotify_etl',     # Nombre de la tarea que aparecerá en Airflow
    python_callable=etl_pipeline,  # Ejecuta la función del archivo ETL_Pipeline.py
    dag=dag,
)

# Define el orden de ejecución de las tareas en el DAG
etl_task
