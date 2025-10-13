# 🗡️ HashiraMart AI System

### *Scalable Data Processing • End-to-End MLOps • Recommender System*

-----

## ⚔️ 1. Overview

**HashiraMart** is a proof-of-concept project designed to showcase a complete, end-to-end, and scalable machine learning system. Unlike a simple ML application, this project demonstrates the full professional lifecycle of an AI product, from large-scale data processing with **Apache Spark** to reproducible model training with **DVC & MLflow**, all containerized with **Docker** and served via a real-time **FastAPI**.

This project is built as an inspirational showcase for a modern data and MLOps platform, covering:

  * **Big Data Processing:** ETL pipelines using Hadoop HDFS, YARN, and PySpark.
  * **End-to-End MLOps:** Reproducible ML pipelines with DVC, experiment tracking with MLflow, and artifact storage with MinIO.
  * **Cloud-Native Architecture:** A centralized cloud database (Supabase) and decoupled services.
  * **Real-time AI Services:** A FastAPI backend serving a recommender system and a sales forecasting model.

-----

## 🧠 2. System Architecture

The architecture is split into two primary, containerized environments that work together: a **Big Data Stack** for processing and a **MLOps & Application Stack** for training, serving, and tracking.

```plaintext
                               .------------------------.
                               |  Cloud Database        |
                               |  (Supabase PostgreSQL) |
                               `----------+-------------'
                                          | (Metadata & App Data)
 .----------------------------------------+----------------------------------------.
 |                                        |                                        |
 |  (1) MLOps & Application Stack         |        (2) Big Data Stack              |
 |  (docker-compose-mlops.yml)            |        (docker-compose-hadoop.yml)     |
 |                                        |                                        |
 | .----------------.  .----------------. | .-----------------.  .----------------. |
 | | FastAPI App    |--| MLflow Server  | | | Spark Job API   |--| YARN Cluster   | |
 | `----------------'  `-------+--------' | `-----------------'  `-------+--------' |
 |                             |           |                              |           |
 `-----------------------------|-----------|------------------------------|-----------'
                               |           |                              |
                               |           | (Clean Data)   (Raw Data)    |
                    .----------+-----------+-------------.  .-------------+----------.
                    |   Artifact & Data Store (MinIO)   |  |   Data Lake (HDFS)     |
                    `-----------------------------------'  `--------------------------'

```

-----

## ⚙️ 3. The ML Pipeline

The pipeline follows a modern, two-stage process that separates data engineering from machine learning.

1.  **Data Processing (Spark):** A PySpark job is submitted to the Hadoop YARN cluster. It reads raw data from HDFS, performs cleaning and feature engineering, and writes the final, model-ready dataset to a bucket in the **MinIO** artifact store. This process is triggered via a simple API.
2.  **Model Training (DVC & Python):** A DVC pipeline (`dvc repro`) is executed.
      * The first stage pulls the clean dataset from MinIO, versioning it with DVC.
      * Subsequent stages use standard Python libraries (LightGBM, Scikit-learn) to train and evaluate the model.
      * All experiment parameters, metrics, and the final model artifact are logged to **MLflow**, which uses MinIO for artifact storage.

### Example `dvc.yaml`

```yaml
stages:
  get_cleaned_data:
    cmd: python ml_pipelines/get_data_from_s3.py
    deps:
      - ml_pipelines/get_data_from_s3.py
    outs:
      - data/processed/recommender_features.parquet

  train_recommender:
    cmd: python ml_pipelines/train_recommender.py
    deps:
      - data/processed/recommender_features.parquet
      - ml_pipelines/train_recommender.py
    outs:
      - models/recommender.pkl
    metrics:
      - reports/metrics.json:
          cache: false
```

-----

## 🧱 4. Backend API (FastAPI)

The core application is a FastAPI server providing a RESTful API for all functionalities.

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/auth/token` | `POST` | Log in a user and receive a JWT access token. |
| `/users` | `POST` | Create a new user (signup). |
| `/users/me` | `GET` | Get the profile of the currently logged-in user. |
| `/products` | `GET`, `POST` | List all products or create a new one. |
| `/products/{id}` | `GET`, `PUT`, `DELETE` | Read, update, or delete a specific product. |
| `/recommendations/me` | `GET` | Get personalized recommendations for the logged-in user. |
| `/forecasts/sales` | `GET` | Get a sales forecast, with optional query parameters. |
| `/jobs/training/recommender` | `POST` | (In Hadoop Stack) An API endpoint to trigger the Spark job. |

-----

## 🧩 5. Tech Stack Summary

| Layer | Technology             | Purpose |
| :--- |:-----------------------| :--- |
| **Data Lake** | Hadoop HDFS            | Distributed storage for raw, large-scale data. |
| **Data Processing**| Apache Spark & YARN    | Large-scale, distributed data cleaning and feature engineering. |
| **Data Versioning** | DVC                    | Version control for datasets and ML models, works with MinIO. |
| **Experiment Tracking** | MLflow                 | Logging and managing ML experiments, models, and metrics. |
| **Artifact Store** | MinIO                  | S3-compatible storage for DVC data, MLflow artifacts, and clean datasets. |
| **Backend API** | FastAPI                | High-performance Python framework for serving the API. |
| **Database** | Neon (Postgres)        | Cloud-hosted database for application data and MLflow/Airflow metadata. |
| **ML Models** | Scikit-learn, LightGBM | Training the recommender and forecasting models. |
| **Containerization** | Docker Compose         | Defining and running the multi-container application environments. |

-----

## 🚀 6. How to Run

This project uses two separate Docker Compose environments. You can run them one at a time to manage system resources.

### Prerequisites

  * Docker and Docker Compose installed.
  * A `.env` file created in the project root with all the necessary credentials (see `.env.example`).
  * A Supabase (or other cloud PostgreSQL) database provisioned.

### Step 1: Run the MLOps & Application Stack

This stack includes the FastAPI application, MLflow, and MinIO. It's used for serving the API, tracking experiments, and interacting with the system.

```bash
# Start all services in the background
docker-compose -f docker-compose-mlops.yml up -d

# Stop all services
docker-compose -f docker-compose-mlops.yml down
```

**Access Points:**

  * **FastAPI App:** `http://localhost:8000/docs`
  * **MLflow UI:** `http://localhost:5000`
  * **MinIO UI:** `http://localhost:9001`

### Step 2: Run the Big Data & Processing Stack

This stack includes Hadoop HDFS, YARN, and Spark. It's used for running large-scale data processing jobs.

```bash
# Start all services in the background
docker-compose -f docker-compose-hadoop.yml up -d

# Stop all services
docker-compose -f docker-compose-hadoop.yml down
```

**Access Points:**

  * **HDFS NameNode UI:** `http://localhost:9870`
  * **YARN ResourceManager UI:** `http://localhost:8088`
  * **Spark Master UI:** `http://localhost:8080` (Note: Port conflicts with Airflow)

### Example Workflow

1.  Start the **Big Data Stack**.
2.  Use the API or `docker exec` to trigger a Spark job that cleans raw data from HDFS and saves the output to MinIO.
3.  Shut down the Big Data Stack.
4.  Start the **MLOps & Application Stack**.
5.  Run `dvc repro` to pull the clean data from MinIO and train a new model, logging the results to MLflow.
6.  Interact with the FastAPI to get recommendations from the newly trained model.