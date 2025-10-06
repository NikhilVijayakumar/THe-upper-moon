from typing import Optional

from pydantic import BaseModel


class RecommendRequest(BaseModel):
    slayer_id: str
    top_k: int = 5


class RecommendationItem(BaseModel):
    weapon_id: str
    weapon_name: str
    score: float


class CombatChatRequest(BaseModel):
    slayer_id: str
    message: str


class EventRequest(BaseModel):
    slayer_id: str
    event_type: str  # e.g., "BATTLE_SUCCESS", "TRAINING_ACTIVITY"
    details: Optional[dict] = None


class ImageGenerateRequest(BaseModel):
    slayer_id: str
    weapon_id: str