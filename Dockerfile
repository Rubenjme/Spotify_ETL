#---------------------------------------------------------------------------------------------------------------------------
# Este archivo Dockerfile se encarga de crear una imagen de Apache Airflow con los paquetes necesarios para ejecutar el DAG.
#---------------------------------------------------------------------------------------------------------------------------

FROM apache/airflow:2.5.1

# Cambiamos al usuario 'airflow' que ya existe en la imagen base
USER airflow

# Copiamos el archivo de requerimientos a una carpeta temporal
COPY requirements.txt /tmp/requirements.txt

# Ajusta la URL de constraints a tu versión de Airflow (2.5.1) y Python (3.7)
ARG AIRFLOW_VERSION=2.5.1
ARG PYTHON_VERSION=3.7
ARG CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"

# Instalamos con pip en modo "user" los paquetes que se encuentran en el archivo de requerimientos y el archivo de constraints de Airflow
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir --user \
       -r /tmp/requirements.txt \
       --constraint "${CONSTRAINT_URL}"
