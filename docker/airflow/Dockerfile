# airflow/Dockerfile
ARG AIRFLOW_VERSION=2.9.2
FROM apache/airflow:${AIRFLOW_VERSION}-python3.10

# Install providers for PostgreSQL and MinIO/S3 connection hooks
# You would also add common packages here (e.g., pandas, scikit-learn)
# if you plan to run simple ML tasks directly inside Airflow workers.
RUN pip install --no-cache-dir \
    apache-airflow-providers-postgres \
    apache-airflow-providers-amazon