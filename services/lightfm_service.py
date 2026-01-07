from datetime import date

import joblib
import numpy as np
from lightfm import LightFM
from sqlalchemy.orm import Session
from database import SessionLocal
from models.model import Game, User

# Chargement du modèle basé sur les noms
model = joblib.load("modeles_lightfm/lightfm_model_name.pkl")
meta = joblib.load("modeles_lightfm/lightfm_meta_name.pkl")

user_map = meta["user_map"]
item_map = meta["item_map"]
index_to_name = meta["index_to_name"]
item_features = meta["item_features"]
n_items = item_features.shape[0]

def calculate_age(birth_date):
    today = date.today()
    if birth_date is None:
        return None
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))



def recommend_for_user(user_id: int | str, top_n: int = 5):
    uid = str(user_id)
    db: Session = SessionLocal()

    if uid not in user_map:
        # Récupérer la date de naissance de l'utilisateur inconnu
        user = db.query(User).filter(User.id_user == user_id).first()
        if user is None or user.date_of_birth is None:
            db.close()
            raise ValueError(f"Utilisateur {user_id} introuvable ou sans date de naissance.")

        user_age = calculate_age(user.date_of_birth)

        # Récupérer les utilisateurs connus par le modèle
        known_user_ids = [int(k) for k in user_map.keys()]
        known_users = db.query(User).filter(User.id_user.in_(known_user_ids)).all()

        # Trouver celui avec l'âge le plus proche
        closest_user = min(
            (u for u in known_users if u.date_of_birth is not None),
            key=lambda u: abs(calculate_age(u.date_of_birth) - user_age),
            default=None
        )

        if closest_user is None:
            db.close()
            raise ValueError("Aucun utilisateur comparable avec âge connu trouvé.")

        uid = str(closest_user.id_user)

    uidx = user_map[uid]
    scores = model.predict(uidx, np.arange(n_items), item_features=item_features)

    seen = model.interactions.tocsr()[uidx].indices if hasattr(model, "interactions") else []
    unseen = np.setdiff1d(np.arange(n_items), seen)
    best = unseen[np.argsort(-scores[unseen])[:top_n]]

    recommended_names = [index_to_name[i] for i in best]
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
