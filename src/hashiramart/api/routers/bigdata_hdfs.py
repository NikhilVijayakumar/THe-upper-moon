import requests
from fastapi import APIRouter, UploadFile, File, HTTPException, Query, status

router = APIRouter(prefix="/big-data", tags=["Big Data Operations"])

# The internal address for the HDFS NameNode service from docker-compose
HDFS_API_URL = "http://namenode:9870/webhdfs/v1"
HDFS_USER = "root"


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_to_hdfs(
        file: UploadFile = File(...),
        hdfs_path: str = Query(default="/user/hashiramart")
):
    """
    Uploads a file to HDFS by proxying the request through the FastAPI app.
    """
    file_content = await file.read()
    target_path = f"{hdfs_path.rstrip('/')}/{file.filename}"
    create_url = f"{HDFS_API_URL}{target_path}?op=CREATE&user.name={HDFS_USER}&overwrite=true"

    try:
        # Step 1: Send a CREATE request to the NameNode.
        create_response = requests.put(create_url, allow_redirects=False)
        create_response.raise_for_status()

        # Extract the redirect URL for the DataNode.
        datanode_url = create_response.headers.get('Location')
        if not datanode_url:
            raise HTTPException(status_code=500, detail="HDFS did not provide a DataNode URL.")

        # Step 2: Send the actual file content to the DataNode URL.
        write_response = requests.put(datanode_url, data=file_content)
        write_response.raise_for_status()

        return {"message": f"Successfully uploaded {file.filename} to {target_path} in HDFS."}

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error communicating with HDFS: {e}")


@router.get("/status")
def hdfs_status(hdfs_path: str = Query(default="/user/hashiramart")):
    """Gets the status and file listing for a directory in HDFS."""
    status_url = f"{HDFS_API_URL}{hdfs_path}?op=LISTSTATUS&user.name={HDFS_USER}"
    try:
        response = requests.get(status_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error communicating with HDFS: {e}")


@router.delete("/delete")
def delete_from_hdfs(
        hdfs_path: str = Query(default="/user/hashiramart", description="The full path of the file or directory to delete in HDFS"),
        recursive: bool = Query(default=False, description="Set to true to delete non-empty directories")
):
    """Deletes a file or directory from HDFS."""
    delete_url = f"{HDFS_API_URL}{hdfs_path}?op=DELETE&user.name={HDFS_USER}&recursive={str(recursive).lower()}"

    try:
        response = requests.delete(delete_url)
        response.raise_for_status()  # Raises an error for non-2xx responses

        # A successful delete returns {"boolean": true}
        if response.json().get("boolean"):
            return {"message": f"Successfully deleted {hdfs_path} from HDFS."}
        else:
            raise HTTPException(status_code=500, detail="HDFS reported a failure but did not return an error.")

    except requests.exceptions.RequestException as e:
        # If the file is not found, HDFS returns a 404, which raise_for_status will catch.
        if e.response and e.response.status_code == 404:
            raise HTTPException(status_code=404, detail=f"File or directory not found at {hdfs_path}")
        raise HTTPException(status_code=500, detail=f"Error communicating with HDFS: {e}")




# @router.post("/process/recommender")
# def process_recommender_data():
#     """Submits a Spark job to clean data for the recommender model."""
#     command = ["spark-submit", "--master", "yarn", "/app/clean_recommender.py"]
#     subprocess.Popen(command)
#     return {"message": "Recommender data processing job submitted."}
#
# @router.post("/process/forecasting")
# def process_forecasting_data():
#     """Submits a Spark job to clean data for the forecasting model."""
#     command = ["spark-submit", "--master", "yarn", "/app/clean_forecasting.py"]
#     subprocess.Popen(command)
#     return {"message": "Forecasting data processing job submitted."}