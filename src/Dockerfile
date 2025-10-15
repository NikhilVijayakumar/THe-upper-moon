# Use a Python base image suitable for a production environment
FROM python:3.10-slim

# Set environment variables to ensure Python output is unbuffered
ENV PYTHONUNBUFFERED 1

# --- Install Dependencies for PostgreSQL (psycopg2-binary) ---
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# --- Set Working Directory ---
WORKDIR /app

# --- Install Python Packages without requirements.txt ---
RUN pip install --no-cache-dir \
    python-multipart \
    pyspark \
    fastapi \
    uvicorn[standard] \
    psycopg2-binary \
    numpy \
    scikit-learn==1.7.2 \
    pandas==2.3.2 \
    lightgbm==4.3.0 \
    dvc[s3]==3.50.1 \
    mlflow==2.15.0 \
    pydantic==2.11.9 \
    pydantic-settings==2.10.1 \
    python-dotenv==1.1.1 \
    pyyaml==6.0.2 \
    pickle-mixin==1.0.2 \
    minio==7.2.16 \
    passlib==1.7.4 \
    python-jose==3.5.0

# --- Copy Application Code ---
COPY . /app

# --- Expose Port ---
EXPOSE 8000

# --- Entrypoint/Command ---
CMD ["uvicorn", "hashiramart.api.app:app", "--host", "0.0.0.0", "--port", "8000"]

