from fastapi import APIRouter, Depends

from hashiramart.security.authentication import get_current_user

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])

@router.get("/me")
def get_my_recommendations(current_user: dict = Depends(get_current_user)):
    user_name = current_user.get("username")
    # ... logic to generate recommendations for user_name
    return {"user": user_name, "recommendations": [...]}