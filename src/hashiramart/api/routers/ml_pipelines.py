import subprocess
from fastapi import APIRouter, HTTPException, status

router = APIRouter(prefix="/pipelines", tags=["ML Pipelines"])


@router.post("/run", status_code=status.HTTP_202_ACCEPTED)
def trigger_dvc_pipeline():
    """
    Triggers the full DVC pipeline (`dvc repro`) in the background.
    This will pull the latest data from MinIO and retrain the models.
    """
    command = ["dvc", "repro"]

    try:
        # Use Popen to run the command in the background
        # The API will return a response immediately without waiting.
        print(f"Executing command: {' '.join(command)}")
        subprocess.Popen(
            command,
            cwd="/app"  # Run the command from the project's root directory inside the container
        )
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="'dvc' command not found. Is DVC installed in the container?")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start DVC pipeline: {str(e)}")

    return {"message": "DVC pipeline execution triggered successfully."}