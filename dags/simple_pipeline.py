from airflow.decorators import dag, task
from datetime import datetime


# Define the DAG structure
@dag(
    dag_id="simple_environment_check",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["mlops", "check"],
)
def simple_environment_check_pipeline():
    """
    A simple demonstration DAG to verify that the Airflow Webserver and Scheduler
    are running correctly and mounting the 'dags' volume.
    It also checks if the environment variables for MLflow are successfully loaded.
    """

    @task(task_id="check_mlops_env_vars")
    def check_status():
        """
        Prints key environment variables to the logs to confirm the DAG can access
        the necessary connection strings for MLflow and MinIO.
        """
        import os

        # Check if the required environment variables are present
        mlflow_uri = os.environ.get('MLFLOW_TRACKING_URI', 'NOT SET')
        s3_endpoint = os.environ.get('MLFLOW_S3_ENDPOINT_URL', 'NOT SET')

        print("--- DAG RUN SUCCESSFUL ---")
        print("Airflow scheduler detected this file and started the run.")
        print(f"MLflow URI: {mlflow_uri}")
        print(f"MinIO S3 Endpoint: {s3_endpoint}")

        if 'NOT SET' in [mlflow_uri, s3_endpoint]:
            raise Exception("Critical MLflow/MinIO environment variable is missing!")

        return "Environment check passed."

    # Set the task order
    check_status()


# Instantiate the DAG
simple_environment_check_pipeline()
