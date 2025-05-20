from sqlalchemy.orm import Session
from sqlalchemy import func
from models.model import Game
from sqlalchemy.orm import joinedload



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
