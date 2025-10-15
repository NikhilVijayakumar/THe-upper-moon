import requests
import uuid
from fastapi import APIRouter, HTTPException, status

router = APIRouter(prefix="/jobs", tags=["Spark Jobs"])

# The internal address for the YARN ResourceManager's REST API
YARN_API_URL = "http://resourcemanager:8088/ws/v1/cluster/apps"
SPARK_SCRIPT_PATH = "/app/process_data.py"  # The path to your script in the spark-master container


def submit_spark_job(task_name: str):
    """
    Constructs a JSON payload and submits a Spark application to the YARN REST API.
    """
    # This is the spark-submit command that YARN will execute on the cluster.
    # Note that it still runs your process_data.py script, which reads the yaml config.
    spark_command = (
        f"/opt/spark/bin/spark-submit "
        f"--master yarn "
        f"--deploy-mode cluster "
        f"{SPARK_SCRIPT_PATH} "
        f"--task {task_name}"
    )

    # This is the JSON payload that the YARN REST API expects
    payload = {
        "application-id": f"hashiramart-{task_name}-{uuid.uuid4()}",
        "application-name": f"HashiraMart-{task_name}-Processing",
        "am-container-spec": {
            "commands": {
                "command": spark_command
            }
        },
        "application-type": "SPARK"
    }

    try:
        response = requests.post(YARN_API_URL, json=payload, headers={'Content-Type': 'application/json'})
        response.raise_for_status()

        # YARN API returns a 202 Accepted on success and includes the app ID in the headers
        app_id = response.headers.get('Location', '').split('/')[-1]
        return {"message": f"{task_name.capitalize()} processing job submitted successfully.", "application_id": app_id}

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to submit job to YARN: {str(e)}")


@router.post("/process/recommender", status_code=status.HTTP_202_ACCEPTED)
def process_recommender_data():
    """Submits a Spark job to clean data for the recommender model."""
    return submit_spark_job(task_name="recommender")


@router.post("/process/forecasting", status_code=status.HTTP_202_ACCEPTED)
def process_forecasting_data():
    """Submits a Spark job to clean data for the forecasting model."""
    return submit_spark_job(task_name="forecasting")