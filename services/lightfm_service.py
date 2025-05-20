import joblib
import numpy as np
from lightfm import LightFM
from sqlalchemy.orm import Session
from database import SessionLocal
from models.model import Game

# Chargement du modèle basé sur les noms
model = joblib.load("modeles_lightfm/lightfm_model_name.pkl")
meta = joblib.load("modeles_lightfm/lightfm_meta_name.pkl")

user_map = meta["user_map"]
item_map = meta["item_map"]
index_to_name = meta["index_to_name"]
item_features = meta["item_features"]
n_items = item_features.shape[0]


def recommend_for_user(user_id: int | str, top_n: int = 5):
    uid = str(user_id)
    if uid not in user_map:
        raise ValueError(f"user_id {uid} non présent dans le modèle.")

    uidx = user_map[uid]
    scores = model.predict(uidx, np.arange(n_items), item_features=item_features)

    # Détection des jeux déjà vus
    seen = model.interactions.tocsr()[uidx].indices if hasattr(model, "interactions") else []
    unseen = np.setdiff1d(np.arange(n_items), seen)
    best = unseen[np.argsort(-scores[unseen])[:top_n]]

    # Obtenir les noms des jeux recommandés
    recommended_names = [index_to_name[i] for i in best]

    db: Session = SessionLocal()
    jeux = db.query(Game).filter(Game.name.in_(recommended_names)).all()

    results = []
    for jeu in jeux:
        jeu_dict = {
            "app_id": jeu.app_id,
            "name": jeu.name,
            "summary": jeu.game_summary,
            "storyline": jeu.storyline,
            "cover_url": jeu.cover_url,
            "artwork_url": jeu.artwork_url,
            "website": jeu.website,
            "developer": jeu.developer.name_developer if jeu.developer else None,
            "genres": [genre.name_genre for genre in jeu.genres],
            "platforms": [platform.nom_platform for platform in jeu.platforms],
            "game_modes": [mode.nom_game_mode for mode in jeu.game_modes],
            "themes": [theme.nom_theme for theme in jeu.themes],
            "perspectives": [persp.nom_perspective for persp in jeu.perspectives],
        }
        results.append(jeu_dict)

    db.close()
    return results
