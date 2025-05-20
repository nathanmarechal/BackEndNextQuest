from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from services.game_service import get_game_by_name, deslugify

router = APIRouter(prefix="/game", tags=["Game"])

@router.get("/{name}", response_model=dict)
def get_game(name: str, db: Session = Depends(get_db)):
    print(f"🔍 Slug reçu : {name}")
    actual_name = deslugify(name)
    print(f"🔄 Déslugifié : {actual_name}")
    result = get_game_by_name(actual_name, db)
    if not result:
        raise HTTPException(status_code=404, detail="Jeu non trouvé")
    return result