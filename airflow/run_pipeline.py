import mlflow
import subprocess
from prefect import flow, task

# Configure MLflow to connect to your MLflow container
mlflow.set_tracking_uri("http://mlflow:5000")


# Necessary for MLflow to talk to MinIO inside the container
# This is handled via environment variables in docker-compose for the agent

@task
def pull_data():
    """Runs dvc pull to get the latest data."""
    print("Pulling data with DVC...")
    subprocess.run(["dvc", "pull", "-v"], check=True, cwd="/app/hashiramart")
    print("Data pulled successfully.")
    return True


@task
def train_model(data_pulled: bool):
    """A placeholder task for training a model and tracking with MLflow."""
    if not data_pulled:
        return

    print("Starting model training...")
    with mlflow.start_run():
        mlflow.set_tag("model", "example_model")
        mlflow.log_param("learning_rate", 0.01)

        # --- YOUR TRAINING LOGIC HERE ---
        # e.g., import your training script from /app/hashiramart

        mlflow.log_metric("accuracy", 0.95)
        print("Model trained and tracked in MLflow.")


@flow(name="ML Training Pipeline")
def ml_pipeline():
    """The main MLOps pipeline flow."""
    data_pulled = pull_data()
    train_model(data_pulled)


# This allows you to run the script directly for testing if needed
if __name__ == "__main__":
    ml_pipeline()