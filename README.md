Of course. It's great that you've expanded the project's scope. Here is the updated documentation that integrates the synthetic data generator, the forecasting model, and the LLM chat agent into your `README.md`.

I have added a new section for the LLM Chat Agent and updated the Overview, System Architecture, ML Pipeline, Backend API, and Tech Stack sections to reflect all your additions.

-----

# 🗡️ HashiraMart AI System

### *Synthetic Data Generation • Scalable Data Processing • End-to-End MLOps • Recommender, Forecaster & LLM Agent*

-----

## ⚔️ 1. Overview

**HashiraMart** is a proof-of-concept project designed to showcase a complete, end-to-end, and scalable machine learning system. This project demonstrates the full professional lifecycle of an AI product, from large-scale data processing with **Apache Spark** to reproducible model training with **DVC & MLflow**, all containerized with **Docker** and served via a real-time **FastAPI**.

This project is built as an inspirational showcase for a modern data and MLOps platform, covering:

  * **Synthetic Data Generation:** A custom script to generate realistic user interaction and sales data for model training.
  * **Big Data Processing:** ETL pipelines using Hadoop HDFS, YARN, and PySpark to clean and prepare data at scale.
  * **End-to-End MLOps:** Reproducible ML pipelines with DVC, experiment tracking with MLflow, and artifact storage with MinIO.
  * **Cloud-Native Architecture:** A centralized cloud database (e.g., Neon) and decoupled services.
  * **Real-time AI Services:** A FastAPI backend serving multiple models:
      * An ML-based **Recommender System**.
      * An ML-based **Sales Forecasting Model**.
      * An **LLM-powered Chat Agent** for product inquiries.

-----

## 🧠 2. System Architecture

The architecture begins with synthetic data generation and is split into two primary containerized environments: a **Big Data Stack** for processing and a **MLOps & Application Stack** for training, serving, and tracking.

```plaintext
[Synthetic Data Gen]
        |
        v
 [Data Lake (HDFS)] <--.
        ^             | (Raw Data)
        |             |
 .------+----------------------------------------+----------------------------------------.
 |      | (Metadata & App Data)                  |                                        |
 | .----+-----------.                            |        (2) Big Data Stack              |
 | | Cloud Database |                            |        (docker-compose-hadoop.yml)     |
 | | (Neon Postgres)|                            |                                        |
 | `----------------'                            | .-----------------.  .----------------. |
 |                                               | | Spark Job API   |--| YARN Cluster   | |
 |  (1) MLOps & Application Stack                | `-----------------'  `-------+--------' |
 |  (docker-compose-mlops.yml)                   |                              |           |
 |                                               `------------------------------|-----------'
 | .--------------------------.  .----------------.                             |
 | | FastAPI App              |--| MLflow Server  |                             |
 | | (Recommender, Forecaster,|  `-------+--------'                             |
 | |  LLM Chat Agent)         |          |                                      |
 | `--------------------------'          |           (Clean Data)               |
 `---------------------------------------|--------------------------------------'
                                         |
                              .----------+-----------.
                              | Artifact Store (MinIO) |
                              `------------------------'
```

-----

## ⚙️ 3. Data & ML Pipelines

The pipeline follows a multi-stage process that separates data generation, data engineering, and machine learning.

### 3.1. Synthetic Data Generation

The entire workflow is seeded by a custom Python script. This generator creates two types of realistic data:

  * **Interaction Data:** User views, clicks, and purchases for training the recommender system.
  * **Time-Series Sales Data:** Historical sales records for training the forecasting model.
    This generated raw data is then uploaded to the **Hadoop HDFS** data lake to simulate a real-world data source.

### 3.2. Data Processing (Spark)

A PySpark job is submitted to the Hadoop YARN cluster. It reads raw data from HDFS, performs cleaning and feature engineering tailored to each model's needs, and writes the final, model-ready datasets (e.g., `recommender_features.parquet`, `forecasting_features.csv`) to a bucket in the **MinIO** artifact store.

### 3.3. Model Training (DVC & Python)

We manage two distinct model training pipelines using DVC (`dvc repro`):

1.  **Recommender Model:** A `dvc` stage pulls the clean interaction data from MinIO and trains a **LightGBM** model to predict user preferences.
2.  **Forecasting Model:** A separate `dvc` stage pulls the clean sales data from MinIO and trains a time-series model using **Scikit-learn** to predict future sales.

All experiment parameters, metrics, and final model artifacts for both pipelines are logged to **MLflow**.

-----

## 🤖 4. LLM Product Chat Agent

To enhance the user experience, the platform includes an intelligent chat agent powered by a Large Language Model (LLM).

  * **Purpose:** Acts as an AI sales assistant, answering user questions about products in a conversational manner.
  * **Design:** The agent uses a simple Retrieval-Augmented Generation (RAG) pattern. When a user asks a question, the API retrieves the relevant product's description from the database and injects it into a prompt for the LLM. This allows the LLM to provide accurate, context-aware answers based on specific product details.

-----

## 🧱 5. Backend API (FastAPI)

The core application is a FastAPI server providing a RESTful API for all functionalities.

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/auth/token` | `POST` | Log in a user and receive a JWT access token. |
| `/users/me` | `GET` | Get the profile of the currently logged-in user. |
| `/products` | `GET`, `POST` | List all products or create a new one. |
| `/recommendations/me` | `GET` | Get personalized recommendations for the logged-in user. |
| `/forecasts/sales` | `GET` | Get a sales forecast, with optional query parameters. |
| `/chat` | `POST` | Interact with the LLM product chat agent. |
| `/jobs/...` | `POST` | (In Hadoop Stack) API endpoints to trigger data processing jobs. |

-----

## 🧩 6. Tech Stack Summary

| Layer | Technology | Purpose |
| :--- |:---| :--- |
| **Data Lake** | Hadoop HDFS | Distributed storage for raw, large-scale data. |
| **Data Processing**| Apache Spark & YARN | Large-scale, distributed data cleaning and feature engineering. |
| **Data Versioning** | DVC | Version control for datasets and ML models. |
| **Experiment Tracking** | MLflow | Logging and managing ML experiments, models, and metrics. |
| **Artifact Store** | MinIO | S3-compatible storage for all data and model artifacts. |
| **Backend API** | FastAPI | High-performance Python framework for serving the API. |
| **Database** | Neon (Postgres) | Cloud-hosted database for application and metadata storage. |
| **ML Models** | Scikit-learn, LightGBM | Training the recommender and forecasting models. |
| **AI Agent** | LLM (Transformers) | Powers the conversational chat agent for product inquiries. |
| **Containerization** | Docker Compose | Defining and running the multi-container application environments. |

-----

## 🚀 7. How to Run

This project uses two separate Docker Compose environments. You can run them one at a time to manage system resources.

### Prerequisites

  * Docker and Docker Compose installed.
  * A `.env` file created in the project root with all the necessary credentials.
  * A cloud PostgreSQL database (e.g., Neon) provisioned.

### Step 1: Run the MLOps & Application Stack

*(Contains FastAPI, MLflow, MinIO, etc.)*

```bash
docker-compose -f docker-compose-mlops.yml up -d
```

### Step 2: Run the Big Data & Processing Stack

*(Contains Hadoop, YARN, Spark, etc.)*

```bash
docker-compose -f docker-compose-hadoop.yml up -d
```

### Example Workflow

1.  Run the **Synthetic Data Generator** script to create raw data.
2.  Start the **Big Data Stack**.
3.  Use the API to upload the raw data to HDFS and trigger the Spark cleaning job. The clean data is saved to MinIO.
4.  Shut down the Big Data Stack.
5.  Start the **MLOps & Application Stack**.
6.  Run `dvc repro` to pull the clean data from MinIO and train new models, logging results to MLflow.
7.  Interact with the live FastAPI to get recommendations, forecasts, and chat with the AI agent.