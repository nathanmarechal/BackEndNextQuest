from datetime import date, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func

from models.model import Game, Review

def get_top_liked_games_last_7_days(db: Session, limit: int = 30):
    from datetime import date, timedelta
    from sqlalchemy import func
    from models.model import Game, Review

    today = date.today()
    last_week = today - timedelta(days=7)

    subquery = (
        db.query(
            Review.app_id,
            func.count(Review.app_id).label("like_count")
        )
        .filter(Review.isliked == True)
        .filter(Review.date_review >= last_week)
        .group_by(Review.app_id)
        .subquery()
    )

    games = (
        db.query(Game)
        .join(subquery, Game.app_id == subquery.c.app_id)
        .order_by(subquery.c.like_count.desc())
        .limit(limit)
        .all()
    )

    results = []
    for jeu in games:
        jeu_dict = {
            "app_id": jeu.app_id,
            "name": jeu.name,
            "summary": jeu.game_summary,
            "storyline": jeu.storyline,
            "cover_url": jeu.cover_url,
            "artwork_url": jeu.artwork_url,
            "website": jeu.website,
            "developer": jeu.developer.name_developer if jeu.developer else None,
            "genres": [genre.name_genre for genre in jeu.genres] if jeu.genres else [],
            "platforms": [platform.nom_platform for platform in jeu.platforms] if jeu.platforms else [],
            "game_modes": [mode.nom_game_mode for mode in jeu.game_modes] if jeu.game_modes else [],
            "themes": [theme.nom_theme for theme in jeu.themes] if jeu.themes else [],
            "perspectives": [persp.nom_perspective for persp in jeu.perspectives] if jeu.perspectives else [],
        }
        results.append(jeu_dict)

    return results

def get_review_by_game_name_five_per_five(db: Session, name: str, offset: int = 0, limit: int = 5):
    """
    Récupère les critiques d'un jeu par son nom, avec pagination.
    """
    print(f"[DEBUG] Requête pour le nom : {name}")

    try:
        jeu = (
            db.query(Game)
            .filter(func.lower(Game.name) == name.lower())
            .first()
        )
        print(f"[DEBUG] Jeu trouvé : {jeu.name if jeu else 'Aucun'}")
    except Exception as e:
        print(f"[ERROR] Exception SQL : {e}")
        raise

    if not jeu:
        return None

    reviews = (
        db.query(Review)
        .filter(Review.app_id == jeu.app_id)
        .order_by(Review.date_review.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return reviews