from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from database import get_db
from models.model import Review as ReviewModel
from services import review_service
from schemas.schema import Review, GameReviewRequest, LikeRequest, ReviewCreate
from services.review_service import user_has_liked_game, set_review_like, fetch_review_by_game_name_five_per_five, \
    create_review

router = APIRouter(prefix="/review", tags=["Review"])

from schemas.schema import ReviewWithUserName

@router.post("/get_review_by_game_name_five_per_five", response_model=list[ReviewWithUserName])
def get_review_by_game_name_five_per_five(
    request: GameReviewRequest,
    db: Session = Depends(get_db)
):
    print(f"[DEBUG] Requête pour le nom : {request.game_name}")
    try:
        # Appel de la fonction du service
        reviews_with_user = fetch_review_by_game_name_five_per_five(  # Utilisation du nouveau nom
            db=db,
            name=request.game_name,
            offset=request.offset,
            limit=request.limit
        )
        if not reviews_with_user:
            raise HTTPException(status_code=404, detail="Aucune critique trouvée")
        return reviews_with_user
    except HTTPException as http_err:
        print(f"[ERROR] HTTPException : {http_err.detail}")
        raise
    except Exception as e:
        import traceback
        print("❌ ERREUR :", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Erreur interne : " + str(e))

@router.get("/check_like/{user_id}/{app_id}", response_model=int)
def check_like(user_id: int, app_id: int, db: Session = Depends(get_db)):
    return user_has_liked_game(db, user_id, app_id)

@router.post("/like_game", response_model=bool)
def like_game(request: LikeRequest, db: Session = Depends(get_db)):
    return set_review_like(db, request.user_id, request.app_id, request.liked)

@router.post("/post_review", response_model=Review)
def post_review(review_data: ReviewCreate, db: Session = Depends(get_db)):
    try:
        return create_review(
            db=db,
            id_user=review_data.id_user,
            app_id=review_data.app_id,
            review=review_data.review,
            review_score=review_data.review_score,
            date_review=review_data.date_review,
            name_user=review_data.name_user
        )
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        print(f"[ERROR] Exception lors de la création de la revue : {e}")
        raise HTTPException(status_code=500, detail="Erreur interne : " + str(e))