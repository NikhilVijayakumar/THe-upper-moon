import subprocess
from fastapi import APIRouter, UploadFile, File, HTTPException, Query
import os
import shutil

router = APIRouter(prefix="/big-data", tags=["HDFS"])

SHARED_DIR = "/data/raw"
NAME_NODE_CONTAINER = "namenode"

@router.post("/upload/")
async def upload_to_hdfs(file: UploadFile = File(...), hdfs_path: str = Query(default=None)):
    # Save the uploaded file to the shared volume
    local_path = os.path.join(SHARED_DIR, file.filename)
    try:
        with open(local_path, "wb") as out_file:
            shutil.copyfileobj(file.file, out_file)
        hdfs_target = hdfs_path or f"/data/raw/{file.filename}"
        # Run hdfs dfs -put from inside the namenode container
        cmd = ["docker", "exec", NAME_NODE_CONTAINER, "hdfs", "dfs", "-put", "-f", local_path, hdfs_target]
        result = subprocess.run(cmd, text=True, capture_output=True)
        os.remove(local_path)
        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=result.stderr)
        return {"message": f"Uploaded {file.filename} to {hdfs_target}"}
    except Exception as e:
        if os.path.exists(local_path):
            os.remove(local_path)
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/remove/")
def remove_from_hdfs(hdfs_path: str = Query(...)):
    cmd = ["docker", "exec", NAME_NODE_CONTAINER, "hdfs", "dfs", "-rm", "-f", hdfs_path]
    result = subprocess.run(cmd, text=True, capture_output=True)
    if result.returncode != 0:
        raise HTTPException(status_code=404, detail=result.stderr)
    return {"message": f"Removed {hdfs_path} from HDFS."}

@router.get("/status/")
def hdfs_status(hdfs_dir: str = Query(default="/data/raw")):
    cmd = ["docker", "exec", NAME_NODE_CONTAINER, "hdfs", "dfs", "-ls", hdfs_dir]
    result = subprocess.run(cmd, text=True, capture_output=True)
    if result.returncode != 0:
        raise HTTPException(status_code=404, detail=result.stderr)
    files = [line for line in result.stdout.splitlines() if not line.startswith("Found")]
    return {"hdfs_dir": hdfs_dir, "files": files}




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