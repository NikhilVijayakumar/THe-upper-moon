import yaml
import argparse
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, year, month, dayofweek, dayofyear


def process_recommender_data(spark, config):
    """
    Reads raw recommender data from HDFS, creates implicit ratings,
    and writes the cleaned data to MinIO.
    """
    print("--- Starting Recommender Data Processing ---")

    # Define paths from config
    hdfs_base_path = config['hdfs']['base_path']
    recommender_raw_path = config['paths']['recommender_raw']
    minio_base_path = f"s3a://{config['minio']['bucket']}"
    recommender_processed_path = config['paths']['recommender_processed']

    # Read the raw parquet file from HDFS
    print(f"Reading from: {hdfs_base_path + recommender_raw_path}")
    raw_df = spark.read.parquet(hdfs_base_path + recommender_raw_path)

    # Create an implicit rating by counting user-product purchases
    clean_df = raw_df.groupBy("user_id", "product_id").agg(
        count("*").alias("purchase_count_rating")
    )

    # Write the cleaned recommender data to MinIO
    print(f"Writing to: {minio_base_path + recommender_processed_path}")
    clean_df.write.mode("overwrite").parquet(minio_base_path + recommender_processed_path)

    print("--- Recommender Data Processing Complete ---")


def process_forecasting_data(spark, config):
    """
    Reads raw forecasting data from HDFS, engineers date-based features,
    and writes the cleaned data to MinIO.
    """
    print("--- Starting Forecasting Data Processing ---")

    # Define paths from config
    hdfs_base_path = config['hdfs']['base_path']
    forecasting_raw_path = config['paths']['forecasting_raw']
    minio_base_path = f"s3a://{config['minio']['bucket']}"
    forecasting_processed_path = config['paths']['forecasting_processed']

    # Read the raw parquet file from HDFS
    print(f"Reading from: {hdfs_base_path + forecasting_raw_path}")
    raw_df = spark.read.parquet(hdfs_base_path + forecasting_raw_path)

    # Engineer date-based features for the time-series model
    clean_df = raw_df.withColumn("year", year(col("date"))) \
        .withColumn("month", month(col("date"))) \
        .withColumn("day_of_week", dayofweek(col("date"))) \
        .withColumn("day_of_year", dayofyear(col("date")))

    # Write the cleaned forecasting data to MinIO
    print(f"Writing to: {minio_base_path + forecasting_processed_path}")
    clean_df.write.mode("overwrite").parquet(minio_base_path + forecasting_processed_path)

    print("--- Forecasting Data Processing Complete ---")


if __name__ == "__main__":
    # Setup command-line argument parsing
    parser = argparse.ArgumentParser(description="Process data for HashiraMart models.")
    parser.add_argument(
        "--task",
        type=str,
        required=True,
        choices=["recommender", "forecasting"],
        help="The processing task to run ('recommender' or 'forecasting')."
    )
    args = parser.parse_args()

    # Load the configuration from the YAML file
    # The path /app/config/ is where the file is mounted in the spark-master container
    with open('/app/config/spark_config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    minio_cfg = config['minio']

    # Initialize the Spark Session with MinIO S3 configuration
    spark = SparkSession.builder \
        .appName(f"HashiraMart-{args.task.capitalize()}") \
        .config("spark.hadoop.fs.s3a.endpoint", minio_cfg['endpoint']) \
        .config("spark.hadoop.fs.s3a.access.key", minio_cfg['access_key']) \
        .config("spark.hadoop.fs.s3a.secret.key", minio_cfg['secret_key']) \
        .config("spark.hadoop.fs.s3a.path.style.access", "true") \
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
        .getOrCreate()

    print(f"Spark session created. Running task: {args.task}")

    # Execute the correct function based on the --task argument
    if args.task == "recommender":
        process_recommender_data(spark, config)
    elif args.task == "forecasting":
        process_forecasting_data(spark, config)

    spark.stop()
    print("Spark session stopped.")