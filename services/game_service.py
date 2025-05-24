from sqlalchemy.orm import Session
from sqlalchemy import func
from models.model import (
    Game, PlatformGame, Platform, PerspectiveGame, Perspective,
    GenreGame, Genre, Developer, GameModeGame, GameMode, ThemeGame, Theme
)
from sqlalchemy.orm import joinedload

def list_games_service(
    db,
    offset=0,
    limit=10,
    order_by_name=False,
    genre=None,
    platform=None,
    developer=None,
    perspective=None,
    game_mode=None,
    theme=None,
    name=None
):
    query = db.query(Game)

    if name:
        query = query.filter(Game.name.ilike(f"%{name}%"))

    if platform:
        query = query.join(PlatformGame, Game.app_id == PlatformGame.app_id) \
            .join(Platform, PlatformGame.id_platform == Platform.id_platform) \
            .filter(Platform.nom_platform.in_(platform))
    if perspective:
        query = query.join(PerspectiveGame, Game.app_id == PerspectiveGame.app_id) \
            .join(Perspective, PerspectiveGame.id_perspective == Perspective.id_perspective) \
            .filter(Perspective.nom_perspective.in_(perspective))
    if genre:
        query = query.join(GenreGame, Game.app_id == GenreGame.app_id) \
            .join(Genre, GenreGame.id_genre == Genre.id_genre) \
            .filter(Genre.name_genre.in_(genre))
    if developer:
        query = query.join(Developer, Game.id_developer == Developer.id_developer) \
            .filter(Developer.name_developer.in_(developer))
    if game_mode:
        query = query.join(GameModeGame, Game.app_id == GameModeGame.app_id) \
            .join(GameMode, GameModeGame.Id_Game_mode == GameMode.Id_Game_mode) \
            .filter(GameMode.nom_game_mode.in_(game_mode))
    if theme:
        query = query.join(ThemeGame, Game.app_id == ThemeGame.app_id) \
            .join(Theme, ThemeGame.id_theme == Theme.id_theme) \
            .filter(Theme.nom_theme.in_(theme))

    if order_by_name:
        query = query.order_by(Game.name)
    query = query.offset(offset).limit(limit)
    return query.all()

def get_game_by_name(name: str, db: Session):
    print(f"[DEBUG] Requête pour le nom : {name}")

    try:
        jeu = (
            db.query(Game)
            .options(
                joinedload(Game.genres),
                joinedload(Game.platforms),
                joinedload(Game.developer),
                joinedload(Game.game_modes),
                joinedload(Game.themes),
                joinedload(Game.perspectives)
            )
            .filter(func.lower(Game.name) == name.lower())
            .first()
        )
        print(f"[DEBUG] Jeu trouvé : {jeu.name if jeu else 'Aucun'}")
    except Exception as e:
        print(f"[ERROR] Exception SQL : {e}")
        raise

    if not jeu:
        return None

    return {
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


import re
import unicodedata

def deslugify(slug: str) -> str:
    """
    Transforme un slug (ex: 'arma-3', 'call-of-duty-black-ops') en nom de jeu
    plus fidèle pour requêtes SQL, ex: 'Arma 3', 'Call Of Duty Black Ops'.
    """
    # Étape 1 : remplace les tirets par des espaces
    text = slug.replace('-', ' ')

    # Étape 2 : retire accents, caractères spéciaux
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')

    # Étape 3 : met une majuscule à chaque mot
    text = re.sub(r'\b\w', lambda m: m.group().upper(), text)

    # Étape 4 (optionnelle) : normalise les espaces multiples
    text = re.sub(r'\s+', ' ', text).strip()

    return text


def get_game_filters_service(db):
    return {
        "platforms": [p.nom_platform for p in db.query(Platform).all()],
        "perspectives": [p.nom_perspective for p in db.query(Perspective).all()],
        "genres": [g.name_genre for g in db.query(Genre).all()],
        "developers": [d.name_developer for d in db.query(Developer).all()],
        "game_modes": [g.nom_game_mode for g in db.query(GameMode).all()],
        "themes": [t.nom_theme for t in db.query(Theme).all()]
    }