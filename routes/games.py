from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from services.game_service import get_game_by_name, deslugify, get_game_filters_service
from services.game_service import list_games_service
from typing import Optional, List
from schemas.schema import Game
from schemas.schema import GameListRequest



router = APIRouter(prefix="/game", tags=["Game"])

@router.get("/getByName/{name}", response_model=dict)
def get_game(name: str, db: Session = Depends(get_db)):
    print(f"🔍 Slug reçu : {name}")
    actual_name = deslugify(name)
    print(f"🔄 Déslugifié : {actual_name}")
    result = get_game_by_name(actual_name, db)
    if not result:
        raise HTTPException(status_code=404, detail="Jeu non trouvé")
    return result

@router.post("/", response_model=List[Game])
def list_games(
    params: GameListRequest,
    db: Session = Depends(get_db)
):
    print(f"[DEBUG] Params reçus : {params}")
    try:
        result = list_games_service(
            db=db,
            offset=params.offset,
            limit=params.limit,
            order_by_name=params.order_by_name,
            genre=params.genre,
            platform=params.platform,
            developer=params.developer,
            perspective=params.perspective,
            game_mode=params.game_mode,
            theme=params.theme,
            name=params.name
        )
        print(f"[DEBUG] Résultat du service : {result}")
        return result
    except Exception as e:
        print(f"[ERROR] Exception dans list_games : {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/filters", response_model=dict)
def get_game_filters(db: Session = Depends(get_db)):
    try:
        return get_game_filters_service(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))