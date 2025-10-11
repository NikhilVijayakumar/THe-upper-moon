# mlflow_server/Dockerfile
FROM python:3.10-slim

# Install necessary MLflow dependencies (for Postgres and MinIO/S3)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    mlflow \
    psycopg2-binary \
    boto3