from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from database import get_db
from models.model import Review as ReviewModel
from services import review_service
from schemas.schema import Review, GameReviewRequest

router = APIRouter(prefix="/review", tags=["Review"])

from schemas.schema import ReviewWithUserName

@router.post("/get_review_by_game_name_five_per_five", response_model=list[ReviewWithUserName])
def get_review_by_game_name_five_per_five(
    request: GameReviewRequest,
    db: Session = Depends(get_db)
):
    print(f"[DEBUG] Requête pour le nom : {request.game_name}")
    try:
        result = review_service.get_review_by_game_name_five_per_five(
            db=db,
            name=request.game_name,
            offset=request.offset,
            limit=request.limit
        )
        if not result:
            raise HTTPException(status_code=404, detail="Aucune critique trouvée")
        # Ajout du nom utilisateur
        reviews_with_user = [
            {
                "id_user": r.id_user,
                "app_id": r.app_id,
                "review": r.review,
                "review_score": r.review_score,
                "date_review": r.date_review,
                "user_name": r.user.name_user if r.user else ""
            }
            for r in result
        ]
        return reviews_with_user
    except Exception as e:
        import traceback
        print("❌ ERREUR :", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Erreur interne : " + str(e))