from fastapi import FastAPI, APIRouter
import subprocess

router = APIRouter(prefix="/big-data", tags=["Big Data"])

@router.post("/process/recommender")
def process_recommender_data():
    """Submits a Spark job to clean data for the recommender model."""
    command = ["spark-submit", "--master", "yarn", "/app/clean_recommender.py"]
    subprocess.Popen(command)
    return {"message": "Recommender data processing job submitted."}

@router.post("/process/forecasting")
def process_forecasting_data():
    """Submits a Spark job to clean data for the forecasting model."""
    command = ["spark-submit", "--master", "yarn", "/app/clean_forecasting.py"]
    subprocess.Popen(command)
    return {"message": "Forecasting data processing job submitted."}