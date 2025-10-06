import pandas as pd
import numpy as np
import yaml
import os
from sklearn.model_selection import train_test_split

# Define file paths based on the project structure
RAW_DATA_PATH = 'data/raw/raw_data.csv'
PARAMS_PATH = 'params.yaml'
TRAIN_OUTPUT_PATH = 'data/processed/train.csv'
TEST_OUTPUT_PATH = 'data/processed/test.csv'


def prepare_data():
    """
    Loads raw data, performs a basic preparation step, and splits the data
    into training and testing sets based on parameters defined in params.yaml.
    """
    print("--- Starting Data Preparation Stage ---")

    # --- 1. Load Parameters ---
    try:
        with open(PARAMS_PATH, 'r') as f:
            params = yaml.safe_load(f)['prepare']
    except FileNotFoundError:
        print(f"Error: {PARAMS_PATH} not found. Ensure it exists in the root directory.")
        return

    split_ratio = params['split_ratio']
    random_state = params['random_state']
    print(f"Loaded parameters: split_ratio={split_ratio}, random_state={random_state}")

    # --- 2. Load Data ---
    try:
        data = pd.read_csv(RAW_DATA_PATH)
    except FileNotFoundError:
        print(f"Error: {RAW_DATA_PATH} not found.")
        print("Please ensure you have placed your raw data file there.")
        # Create a dummy dataframe for testing if file is missing
        print("Creating dummy data for demonstration...")
        data = pd.DataFrame({
            'feature_1': np.random.rand(100),
            'feature_2': np.random.rand(100),
            'target': np.random.randint(0, 2, 100)
        })
        # Save the dummy data so the next step doesn't fail immediately
        os.makedirs(os.path.dirname(RAW_DATA_PATH), exist_ok=True)
        data.to_csv(RAW_DATA_PATH, index=False)
        print(f"Dummy data saved to {RAW_DATA_PATH}. Please replace it with real data later.")

    print(f"Raw data loaded successfully. Shape: {data.shape}")

    # --- 3. Simple Feature Engineering / Cleaning (Example) ---
    # For a real project, this is where you would handle NaNs, encode variables, etc.
    data['interaction_feature'] = data['feature_1'] * data['feature_2']
    print("Added 'interaction_feature'.")

    # --- 4. Split Data ---
    # Assuming 'target' is the column you want to predict
    X = data.drop('target', axis=1)
    y = data['target']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=split_ratio, random_state=random_state, stratify=y
    )

    # Recombine for saving as CSV
    train_data = pd.concat([X_train, y_train], axis=1)
    test_data = pd.concat([X_test, y_test], axis=1)

    print(f"Train data shape: {train_data.shape}")
    print(f"Test data shape: {test_data.shape}")

    # --- 5. Save Processed Data ---
    os.makedirs(os.path.dirname(TRAIN_OUTPUT_PATH), exist_ok=True)

    train_data.to_csv(TRAIN_OUTPUT_PATH, index=False)
    test_data.to_csv(TEST_OUTPUT_PATH, index=False)

    print(f"Processed training data saved to {TRAIN_OUTPUT_PATH}")
    print(f"Processed testing data saved to {TEST_OUTPUT_PATH}")
    print("--- Data Preparation Complete ---")


if __name__ == "__main__":
    prepare_data()