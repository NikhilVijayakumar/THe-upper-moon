# Use the official Apache Airflow image as the base.
# It's best to pin to a specific version for stable builds.
FROM apache/airflow:3.1.0-python3.12

# Switch to the root user to install system-level packages
USER root

# Install dumb-init, which helps manage processes and signals correctly
RUN apt-get update && apt-get install -y --no-install-recommends dumb-init && apt-get clean

# Switch back to the non-priveleged airflow user
USER airflow

# Copy the requirements file into the container's temp directory
COPY requirements.txt /tmp/requirements.txt

# Install the Python dependencies for your DAGs and tasks
RUN pip install --no-cache-dir --user -r /tmp/requirements.txt

# Set dumb-init as the entrypoint to properly manage the Airflow processes
ENTRYPOINT [ "dumb-init", "--" ]