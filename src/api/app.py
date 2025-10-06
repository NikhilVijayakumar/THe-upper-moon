import os
import json
from contextlib import asynccontextmanager
from typing import List, Optional
from datetime import datetime

from dotenv import load_dotenv
# Database imports
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder

from src.api.db.model import SlayerDB, WeaponDB, InteractionDB, GamificationDB, Base
from src.api.db.request_response import RecommendationItem, RecommendRequest, CombatChatRequest, ImageGenerateRequest, \
    EventRequest

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# MLflow Tracking and MinIO endpoints (for model loading/logging in real app)
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000")
MLFLOW_S3_ENDPOINT_URL = os.getenv("MLFLOW_S3_ENDPOINT_URL", "http://minio:9000")

# --- 1. Database Setup (SQLAlchemy) ---

# The database engine for the HashiraMart application data
if not DATABASE_URL:
    print("FATAL: DATABASE_URL not set. Running in memory mode.")
    # Fallback to in-memory sqlite for local testing if DB_URL is missing
    engine = create_engine("sqlite:///./test.db", connect_args={"check_same_thread": False})
else:
    # Connect to the PostgreSQL app_db service defined in docker-compose
    # The host in DATABASE_URL must be the Docker service name (e.g., 'app_db')
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



# Function to create tables
def create_db_tables():
    """Initializes the database tables if they do not exist."""
    print("Attempting to create database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database initialization complete.")


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- 3. ML Model and LLM/Generative Placeholders ---

# Global variable to hold the loaded recommendation model
RECOMMENDATION_MODEL = None


def load_ml_model():
    """
    Placeholder for loading the LightGBM model from MLflow.
    In a real system, this would use the MLflow API to fetch the 'production' tagged model.
    """
    global RECOMMENDATION_MODEL
    print(f"Loading model from MLflow tracking URI: {MLFLOW_TRACKING_URI}...")

    # Simulate a loaded model object with a simple prediction function
    class DummyModel:
        def predict_proba(self, X):
            # X would be a dataframe of features (slayer + weapon attributes)
            # This returns random scores for demonstration
            import numpy as np
            return np.array([[0.5, np.random.rand()] for _ in range(len(X))])

    RECOMMENDATION_MODEL = DummyModel()
    print("Dummy Recommendation Model loaded successfully.")


async def call_gemini_combat_coach(prompt: str, context: dict) -> str:
    """Placeholder for calling the LLM Core (Gemini API)."""
    print(f"Calling Gemini Combat Coach with prompt: {prompt}")
    # In a real app, this would use the Gemini API (gemini-2.5-flash)

    # Simulating a grounded, contextual response
    weapon_name = context.get('weapon_name', 'your weapon')
    advice = f"Greetings, Slayer! Based on your current focus with {weapon_name}, I recommend practicing the 'Total Concentration Breathing - Constant' exercise for 10 minutes. A strong core is vital for water-style users. Motivational Quote: 'Move your soul, not just your body!'"
    return advice


async def call_imagen_slayer_generator(slayer_details: dict, weapon_name: str) -> str:
    """Placeholder for calling the Generative Image Module (Imagen API)."""
    print(f"Calling Imagen API for visualization...")
    prompt = f"{slayer_details['name']}, {slayer_details['breathing_style']} Breathing, wielding a {weapon_name}, epic cinematic anime art."
    image_url = f"https://placehold.co/400x600/121212/EDEDED?text=AI+GENERATED\n{weapon_name}+SLAYER"
    return image_url


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Initialize the database tables before the app starts accepting requests
    create_db_tables()

    # 2. Load the ML model
    load_ml_model()

    yield




app = FastAPI(title="HashiraMart Backend", version="1.0.0", lifespan=lifespan)



@app.get("/")
def read_root():
    return {"message": "HashiraMart API Operational. Forge your destiny."}


@app.post("/recommend", response_model=List[RecommendationItem], tags=["Recommender"])
def recommend_weapons(req: RecommendRequest, db: SessionLocal = Depends(get_db)):
    """
    Returns top weapon recommendations based on the Slayer's profile
    using the loaded LightGBM model.
    """
    slayer = db.query(SlayerDB).filter(SlayerDB.id == req.slayer_id).first()
    if not slayer:
        raise HTTPException(status_code=404, detail="Slayer not found")

    weapons = db.query(WeaponDB).all()

    if not RECOMMENDATION_MODEL:
        raise HTTPException(status_code=503, detail="Model not loaded")

    # 1. Feature Engineering Placeholder (Convert data into model input X)
    X_features = []
    weapon_map = {}
    for weapon in weapons:
        # Simulate feature creation (Section 3: level, strength, match_style, etc.)
        X_features.append([
            slayer.level, slayer.strength, weapon.weight,
            1 if slayer.breathing_style == weapon.breathing_compatibility else 0
        ])
        weapon_map[weapon.id] = weapon.name

    # 2. Prediction
    # DummyModel.predict_proba returns array([[0.5, score1], [0.5, score2], ...])
    import numpy as np
    X_array = np.array(X_features)
    preds = RECOMMENDATION_MODEL.predict_proba(X_array)[:, 1]

    # 3. Ranking and Formatting
    recommendations = []
    for (weapon, score) in sorted(zip(weapons, preds), key=lambda x: x[1], reverse=True)[:req.top_k]:
        recommendations.append(RecommendationItem(
            weapon_id=weapon.id,
            weapon_name=weapon_map[weapon.id],
            score=float(score)
        ))

    return recommendations


@app.post("/coach/chat", tags=["Combat Coach"])
async def coach_chat(req: CombatChatRequest, db: SessionLocal = Depends(get_db)):
    """
    Interacts with the AI Combat Coach (LLM Core) for personalized advice.
    """
    slayer = db.query(SlayerDB).filter(SlayerDB.id == req.slayer_id).first()
    if not slayer:
        raise HTTPException(status_code=404, detail="Slayer not found")

    # Fetch current weapon (simplistic approach for context)
    current_weapon = db.query(WeaponDB).filter(WeaponDB.id == "katana_001").first()

    # Context for the LLM
    context = {
        "slayer_name": slayer.name,
        "breathing_style": slayer.breathing_style,
        "weapon_name": current_weapon.name if current_weapon else "Unknown Blade"
    }

    # Call the LLM with context injection (Section 5)
    response_text = await call_gemini_combat_coach(req.message, context)

    return {"response": response_text, "context": context}


@app.post("/generate_image", tags=["Generative AI"])
async def generate_image(req: ImageGenerateRequest, db: SessionLocal = Depends(get_db)):
    """
    Generates a custom AI visualization of the Slayer wielding the chosen weapon.
    """
    slayer = db.query(SlayerDB).filter(SlayerDB.id == req.slayer_id).first()
    weapon = db.query(WeaponDB).filter(WeaponDB.id == req.weapon_id).first()

    if not slayer or not weapon:
        raise HTTPException(status_code=404, detail="Slayer or Weapon not found")

    slayer_details = {"name": slayer.name, "breathing_style": slayer.breathing_style}

    # Call the Imagen generator (Section 10)
    image_url = await call_imagen_slayer_generator(slayer_details, weapon.name)

    return {"slayer_id": req.slayer_id, "weapon_name": weapon.name, "image_url": image_url}


@app.post("/events", tags=["Gamification & MLOps"])
def log_event(req: EventRequest, db: SessionLocal = Depends(get_db)):
    """
    Logs interactions and updates the Gamification Engine (Section 8).
    This data feeds into the MLOps retraining loop (Section 11).
    """
    slayer_id = req.slayer_id

    # 1. Update Interactions (for MLOps Retraining Data)
    if req.event_type == "BATTLE_SUCCESS" or req.event_type == "BATTLE_FAILURE":
        outcome = req.event_type == "BATTLE_SUCCESS"
        new_interaction = InteractionDB(
            slayer_id=slayer_id,
            weapon_id=req.details.get("weapon_id"),
            battle_outcome=outcome
        )
        db.add(new_interaction)

    # 2. Update Gamification (Nichirin Points/Rank)
    gamification_entry = db.query(GamificationDB).filter(GamificationDB.slayer_id == slayer_id).first()
    if not gamification_entry:
        gamification_entry = GamificationDB(slayer_id=slayer_id)
        db.add(gamification_entry)
        db.flush()  # Ensure the new entry is available

    points_to_add = 0
    if req.event_type == "BATTLE_SUCCESS":
        points_to_add = 10
    elif req.event_type == "TRAINING_ACTIVITY":
        points_to_add = 1

    if points_to_add > 0:
        gamification_entry.nichirin_points += points_to_add

        # Check for rank update (Section 8 Tiers)
        new_rank = gamification_entry.rank
        if gamification_entry.nichirin_points >= 500:
            new_rank = 'Hashira'
        elif gamification_entry.nichirin_points >= 100:
            new_rank = 'Slayer'
        else:
            new_rank = 'Apprentice'

        if new_rank != gamification_entry.rank:
            gamification_entry.rank = new_rank

    db.commit()
    return {"status": "event logged and profile updated", "points": gamification_entry.nichirin_points,
            "rank": gamification_entry.rank}
