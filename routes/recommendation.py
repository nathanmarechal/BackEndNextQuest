# routes/recommendation.py

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from routes.users import get_db
from services import review_service
from services.lightfm_service import recommend_for_user

router = APIRouter(prefix="/recommendation", tags=["Recommendation"])

class RecommendationRequest(BaseModel):
    user_id: int
    top_n: int = 5

@router.post("/")
def get_recommendations(data: RecommendationRequest):
    try:
        recommandations = recommend_for_user(data.user_id, data.top_n)
        return recommandations
    except ValueError as err:
        raise HTTPException(status_code=404, detail=str(err))

@router.get("/top-liked-last-7-days")
def get_top_liked_games(db: Session = Depends(get_db)):
    try:
        return review_service.get_top_liked_games_last_7_days(db)
    except Exception as e:
        import traceback
        print("❌ ERREUR :", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Erreur interne : " + str(e))
