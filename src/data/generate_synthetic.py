import pandas as pd
import numpy as np
import uuid

# --- Configuration ---
NUM_SLAYERS = 2000
NUM_WEAPONS = 500
NUM_INTERACTIONS = 50000
OUTPUT_DIR = "../../data/raw"
SLAYER_PATH = f"{OUTPUT_DIR}/slayer_profiles.csv"
WEAPON_PATH = f"{OUTPUT_DIR}/weapon_attributes.csv"
INTERACTION_PATH = f"{OUTPUT_DIR}/historical_interactions.csv"


# --- Data Generation Functions ---

def generate_slayers(n):
    """Creates synthetic Slayer profiles."""
    styles = ['Water', 'Flame', 'Thunder', 'Wind', 'Stone', 'Mist', 'Flower', 'Sound', 'Love', 'Serpent']

    slayers = pd.DataFrame({
        'id': [str(uuid.uuid4()) for _ in range(n)],
        'name': [f"Slayer_{i}" for i in range(n)],
        'breathing_style': np.random.choice(styles, n),
        'level': np.random.randint(1, 100, n),
        'strength': np.random.uniform(50, 150, n).round(2),
        'dexterity': np.random.uniform(50, 150, n).round(2),
        'stamina': np.random.uniform(50, 150, n).round(2),
    })
    return slayers


def generate_weapons(n):
    """Creates synthetic Weapon attributes."""
    types = ['Katana', 'Naginata', 'Axe', 'Whip', 'Scimitar']
    compatibility = ['Water', 'Flame', 'Thunder', 'Wind', 'Stone', 'Mist', 'Flower', 'Sound', 'Love', 'Serpent', 'None']

    weapons = pd.DataFrame({
        'id': [f"WPN_{i:04d}" for i in range(n)],
        'name': [f"NichirinBlade_{i}" for i in range(n)],
        'type': np.random.choice(types, n),
        'weight': np.random.uniform(1.0, 3.5, n).round(2),
        'sharpness': np.random.uniform(0.7, 1.0, n).round(2),
        'price': np.random.randint(500, 5000, n),
        'breathing_compatibility': np.random.choice(compatibility, n),
    })
    return weapons


def generate_interactions(n, slayer_ids, weapon_ids):
    """Creates synthetic historical battle outcomes (for target variable)."""

    interactions = pd.DataFrame({
        'slayer_id': np.random.choice(slayer_ids, n),
        'weapon_id': np.random.choice(weapon_ids, n),
    })

    # Introduce correlation: match style gets a higher chance of success
    def determine_outcome(row):
        # Placeholder for actual logic: 60% base success, +20% for compatibility
        base_success_prob = 0.6
        compatibility_bonus = 0.2 if np.random.rand() < 0.2 else 0  # 20% chance of being a good match
        prob = base_success_prob + compatibility_bonus
        return np.random.rand() < prob

    # For a large dataset, this apply is slow, but demonstrates the concept
    interactions['battle_outcome'] = interactions.apply(determine_outcome, axis=1)
    interactions['timestamp'] = pd.to_datetime('2024-01-01') + pd.to_timedelta(np.random.randint(0, 365, n), unit='D')

    # Convert boolean to integer (1 for Success, 0 for Failure)
    interactions['battle_outcome'] = interactions['battle_outcome'].astype(int)

    return interactions


# --- Main Execution ---

if __name__ == "__main__":
    import os

    # 1. Ensure the output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print(f"Generating {NUM_SLAYERS} slayer profiles...")
    slayer_df = generate_slayers(NUM_SLAYERS)

    print(f"Generating {NUM_WEAPONS} weapon attributes...")
    weapon_df = generate_weapons(NUM_WEAPONS)

    print(f"Generating {NUM_INTERACTIONS} historical interactions...")
    interaction_df = generate_interactions(
        NUM_INTERACTIONS, slayer_df['id'].unique(), weapon_df['id'].unique()
    )

    # 2. Save the data to CSV files
    slayer_df.to_csv(SLAYER_PATH, index=False)
    weapon_df.to_csv(WEAPON_PATH, index=False)
    interaction_df.to_csv(INTERACTION_PATH, index=False)

    print("\nSynthetic data generation complete.")
    print(f"Slayer data saved to: {SLAYER_PATH}")
    print(f"Weapon data saved to: {WEAPON_PATH}")
    print(f"Interaction data saved to: {INTERACTION_PATH}")