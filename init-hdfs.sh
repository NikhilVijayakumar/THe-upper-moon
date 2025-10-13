#!/bin/bash

# Wait a moment for the NameNode to be fully ready
sleep 15

# Create the necessary base directory in HDFS
echo "Creating HDFS directory /user/hashiramart..."
hdfs dfs -mkdir -p /user/hashiramart

echo "HDFS initialization complete. Directory is ready."