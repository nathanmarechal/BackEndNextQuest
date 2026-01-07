from datetime import date, timedelta
from xmlrpc.client import DateTime

from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from models.model import Game, Review, IsLiked, User


def fetch_review_by_game_name_five_per_five(db: Session, name: str, offset: int = 0, limit: int = 5):
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
        db.query(
            Review.id_user,
            Review.app_id,
            Review.review,
            Review.review_score,
            Review.date_review,
            IsLiked.isliked_value,
            User.name_user  # Ajout du champ `user_name`
        )
        .join(IsLiked, (Review.app_id == IsLiked.app_id) & (Review.id_user == IsLiked.id_user), isouter=True)        .join(User, Review.id_user == User.id_user)  # Jointure avec `User`
        .filter(Review.app_id == jeu.app_id)
        .order_by(Review.date_review.desc())
        .offset(offset)
        .limit(limit)
        .distinct()
        .all()
    )

    # Formatage des résultats pour inclure les informations de `user_name`
    formatted_reviews = [
        {
            "id_user": id_user,
            "app_id": app_id,
            "review": review,
            "review_score": review_score,
            "date_review": date_review,
            "isliked": isliked_value if isliked_value is not None else False,
            "user_name": user_name  # Remplacement de 'User.name_user' par 'user_name'
        }
        for id_user, app_id, review, review_score, date_review, isliked_value, user_name in reviews
    ]
    for review in formatted_reviews:
        print(review)

    return formatted_reviews

def create_review(
    db: Session,
    id_user: int,
    app_id: int,
    review: str,
    review_score: int,
    date_review: DateTime,
    name_user: str
):
    print(f"[DEBUG] Données reçues : id_user={id_user}, app_id={app_id}, review={review}, review_score={review_score}, date_review={date_review}, name_user={name_user}")

    # Vérification si l'utilisateur a déjà laissé un avis pour ce jeu
    existing_review = db.query(Review).filter(
        Review.id_user == id_user,
        Review.app_id == app_id
    ).first()

    if existing_review:
        raise HTTPException(status_code=400, detail="Vous avez déjà laissé un avis pour ce jeu.")

    # Création de la nouvelle revue
    new_review = Review(
        id_user=id_user,
        app_id=app_id,
        review=review,
        review_score=review_score,
        date_review=date_review or date.today(),
    )
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    print(f"[DEBUG] Critique créée : {new_review}")
    return new_review


def user_has_liked_game(db: Session, user_id: int, app_id: int) -> int:
    isliked = db.query(IsLiked).filter(
        IsLiked.id_user == user_id,
        IsLiked.app_id == app_id
    ).first()

    if not isliked:
        return 0
    return 1 if isliked.isliked_value else -1

def set_review_like(db: Session, user_id: int, app_id: int, liked: bool) -> bool:
    isliked = db.query(IsLiked).filter(
        IsLiked.id_user == user_id,
        IsLiked.app_id == app_id
    ).first()

    if isliked:
        isliked.isliked_value = liked
    else:
        isliked = IsLiked(
            id_user=user_id,
            app_id=app_id,
            isliked_value=liked
        )
        db.add(isliked)

    db.commit()
    return liked


def get_top_liked_games_last_7_days(db: Session, limit: int = 90):
    from datetime import date, timedelta
    from sqlalchemy import func

    today = date.today()
    last_week = today - timedelta(days=1000)

    subquery = (
        db.query(
            IsLiked.app_id,
            func.count(IsLiked.app_id).label("like_count")
        )
        .join(Review, (IsLiked.app_id == Review.app_id) & (IsLiked.id_user == Review.id_user))
        .filter(IsLiked.isliked_value == True)
        .filter(Review.date_review >= last_week)
        .group_by(IsLiked.app_id)
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

    print(len(results))

    return results
