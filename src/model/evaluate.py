import pandas as pd
import numpy as np
import yaml
import json
import joblib
import os
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import mlflow
import mlflow.sklearn

# Define file paths based on the project structure
TEST_DATA_PATH = 'data/processed/test.csv'
MODEL_PATH = 'model/recommender_model.pkl'
PARAMS_PATH = 'params.yaml'
METRICS_OUTPUT_PATH = 'metrics.json'


def evaluate_model():
    """
    Loads test data and the trained model, calculates performance metrics,
    saves metrics for DVC, and logs everything to MLflow.
    """
    print("--- Starting Model Evaluation Stage ---")

    # --- 1. Load Data and Model ---
    try:
        test_data = pd.read_csv(TEST_DATA_PATH)
        model = joblib.load(MODEL_PATH)
        with open(PARAMS_PATH, 'r') as f:
            params = yaml.safe_load(f)
    except FileNotFoundError as e:
        print(f"Error loading required file: {e}")
        return

    # Assuming the target column is 'target' as defined in prepare.py
    X_test = test_data.drop('target', axis=1)
    y_test = test_data['target']

    # --- 2. Make Predictions and Calculate Metrics ---
    predictions = model.predict(X_test)

    metrics = {
        'accuracy': accuracy_score(y_test, predictions),
        'precision': precision_score(y_test, predictions, zero_division=0),
        'recall': recall_score(y_test, predictions, zero_division=0),
        'f1_score': f1_score(y_test, predictions, zero_division=0)
    }

    print("\nCalculated Metrics:")
    for key, value in metrics.items():
        print(f"  {key}: {value:.4f}")

    # --- 3. DVC Metric Logging (Output to metrics.json) ---
    with open(METRICS_OUTPUT_PATH, 'w') as outfile:
        json.dump(metrics, outfile, indent=4)

    print(f"\nMetrics saved for DVC to {METRICS_OUTPUT_PATH}")

    # --- 4. MLflow Tracking ---
    try:
        # Set the MLflow tracking URI to use the Docker service name
        # The MLFLOW_TRACKING_URI environment variable is passed via docker-compose
        mlflow.set_tracking_uri(os.environ.get("MLFLOW_TRACKING_URI"))
        mlflow.set_experiment("DVC-MLOps-Pipeline")

        with mlflow.start_run() as run:
            print(f"\nMLflow Run ID: {run.info.run_id}")

            # Log Parameters (from both prepare and train stages)
            mlflow.log_params(params.get('prepare', {}))
            mlflow.log_params(params.get('train', {}))

            # Log Metrics
            mlflow.log_metrics(metrics)

            # Log Model Artifact
            mlflow.sklearn.log_model(
                sk_model=model,
                artifact_path="model",
                registered_model_name="RecommenderModel"
            )

        print("Successfully logged metrics, parameters, and model to MLflow.")

    except Exception as e:
        print(f"MLflow logging failed (Is MLflow container healthy?): {e}")

    print("--- Model Evaluation Complete ---")


if __name__ == "__main__":
    evaluate_model()