# Use a Python base image suitable for a production environment
FROM python:3.10-slim

# Set environment variables to ensure Python output is unbuffered
ENV PYTHONUNBUFFERED 1

# --- Install Dependencies for PostgreSQL (psycopg2-binary) ---
# We need system packages (gcc, libpq-dev) to build the PostgreSQL adapter.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# --- Set Working Directory ---
# The build context (../src) will be copied here.
WORKDIR /app

# --- Install Python Packages ---
# Install all required Python packages directly in the image
RUN pip install --no-cache-dir \
    fastapi==0.111.0 \
    uvicorn[standard]==0.29.0 \
    sqlalchemy==2.0.30 \
    psycopg2-binary==2.9.9 \
    pydantic==2.7.4

# --- Copy Application Code ---
# Copy the source code from the build context (../src) into the container's /app directory
COPY . /app

# --- Expose Port ---
# Inform Docker that the container listens on the specified port
EXPOSE 8000

# --- Entrypoint/Command ---
# The command defined here is typically overridden by docker-compose, but
# serves as a good default for running the application.
# The command is: uvicorn api.app:app --host 0.0.0.0 --port 8000
CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8000"]
