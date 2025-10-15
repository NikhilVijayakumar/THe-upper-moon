
## \#\# The Big Data Platform (The "Data Warehouse")

To train powerful models without relying on pre-existing historical data, our platform's lifecycle begins with a **synthetic data generator**. This generator creates realistic raw user and sales data, which is then fed into our Big Data Platform. The platform's primary role is to act as a "data factory," refining this synthetic data into clean, structured datasets ready for machine learning.

[Image of a data warehouse pipeline]

### **Hadoop Distributed File System (HDFS): The Data Lake**

In our e-commerce app, HDFS serves as the **data lake**—a vast, central repository for storing all raw historical data. For this proof-of-concept, we populate the data lake with data created by our **synthetic data generator**, which simulates realistic user clicks, product views, and transactions over many years. HDFS is designed for this scale and provides **fault tolerance** by replicating data across multiple nodes.

**In Practice:**
Our `big-data` API provides a gateway to manage the data lake.

  * The `POST /upload` endpoint uses the built-in WebHDFS REST API to stream the **synthetically generated** raw data files directly into HDFS.
  * The `GET /status` and `DELETE /delete` endpoints provide the necessary tools to browse and manage these files within our data lake.

<!-- end list -->

```python
# From the big-data router, this talks to HDFS
HDFS_API_URL = "http://namenode:9870/webhdfs/v1"
```

-----

### **YARN (Yet Another Resource Negotiator): The Cluster's Operating System**

YARN is the brain of our data platform. It acts as the cluster's **resource manager**, deciding how to allocate CPU and memory to different jobs. It consists of:

  * A central **ResourceManager** (the master) that accepts job requests.
  * Several **NodeManagers** (the workers) that run the actual tasks.

**In Practice:**
Our `jobs` API is the control panel for YARN.

  * When a request is sent to `POST /process/recommender`, our FastAPI application sends a job submission request directly to the **ResourceManager's** REST API.
  * The JSON payload in this request tells YARN to launch a new **Application Master** specifically for our Spark processing job. This is how our application "commands" the cluster to start working.

<!-- end list -->

```python
# From the jobs router, this talks to YARN
YARN_API_URL = "http://resourcemanager:8088/ws/v1/cluster/apps"
```

-----

### **Apache Spark: The Processing Engine**

Spark is the fast, in-memory engine that performs the actual data processing. It reads the raw **synthetic data** from HDFS, cleans it, and engineers the features needed for our ML models. We use Spark's modern DataFrame API, which is built on several core concepts:

  * **Lazy Evaluation:** In our `process_data.py` script, operations like `.groupBy()` (for the recommender) and `.withColumn()` (for the forecaster) are **transformations**. Spark doesn't run them immediately; it builds an optimized plan called an **RDD lineage graph**.
  * **Actions:** The job only begins when an **action** like `.write.parquet()` is called. This allows Spark to execute the entire plan efficiently.
  * **Fault Tolerance:** If a node fails during processing, Spark uses its **RDD lineage** to automatically re-compute only the lost partitions of data, ensuring the job can finish successfully.

**In Practice:**
The `spark-submit` command in our `jobs` API payload kicks off the `process_data.py` script. This script reads the raw data from HDFS, applies a series of **transformations** to clean it, and then triggers an **action** to write the final, clean dataset to our MinIO artifact store, ready for the next stage of the ML pipeline.