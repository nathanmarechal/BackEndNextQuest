import pandas as pd
import numpy as np
import mysql.connector
import joblib
import time

from sklearn.decomposition import PCA
from sklearn.cluster import MiniBatchKMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler
from scipy.sparse import csr_matrix, hstack

from lightfm import LightFM
from lightfm.data import Dataset

def get_training_dataframe_from_db():
    conn = mysql.connector.connect(
        host="localhost",
        user="nathan",
        password="password",
        database="NextQuest"
    )
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            g.name AS app_name,
            r.review AS review_text,
            r.review_score,
            1 AS review_votes,
            g.app_id,
            g.name,
            NULL AS release_year,
            g.game_summary,
            g.storyline,
            g.cover_url,
            g.artwork_url,
            g.website,
            d.name_developer AS developer_grouped
        FROM review r
        JOIN games g ON r.app_id = g.app_id
        LEFT JOIN developers d ON g.id_developer = d.id_developer
    """)
    data = cursor.fetchall()
    df = pd.DataFrame(data)

    def get_relation_column(table, col_name, alias):
        cursor.execute(f"""
            SELECT g.app_id, GROUP_CONCAT(t.{col_name} SEPARATOR ', ') AS {alias}
            FROM {table}_games g
            JOIN {table} t ON g.id_{table[:-1]} = t.id_{table[:-1]}
            GROUP BY g.app_id
        """)
        return {row["app_id"]: row[alias] for row in cursor.fetchall()}

    def get_game_modes_column():
        cursor.execute("""
            SELECT g.app_id, GROUP_CONCAT(m.nom_game_mode SEPARATOR ', ') AS game_modes
            FROM game_modes_games g
            JOIN game_modes m ON g.Id_Game_mode = m.Id_Game_mode
            GROUP BY g.app_id
        """)
        return {row["app_id"]: row["game_modes"] for row in cursor.fetchall()}

    for col, query_func in [
        ("genres", lambda: get_relation_column("genres", "name_genre", "genres")),
        ("platforms", lambda: get_relation_column("platforms", "nom_platform", "platforms")),
        ("game_modes", get_game_modes_column),
        ("perspectives", lambda: get_relation_column("perspectives", "nom_perspective", "perspectives")),
        ("themes", lambda: get_relation_column("themes", "nom_theme", "themes")),
    ]:
        mapping = query_func()
        df[col] = df["app_id"].map(mapping)

    df["rating"] = None
    df["aggregated_rating"] = None
    df["sentiment"] = "positive"
    df.dropna(subset=["review_text", "review_score"], inplace=True)
    df.drop_duplicates(subset=["review_text", "app_id"], inplace=True)

    cursor.close()
    conn.close()
    return df.reset_index(drop=True)


def train_and_save_lightfm_model():
    df = get_training_dataframe_from_db()

    # 2.1 TF-IDF + Numérique → item features
    for col in ['genres', 'themes', 'game_modes', 'perspectives']:
        df[col] = df[col].fillna("")
    df["text_features"] = df["genres"] + " " + df["themes"] + " " + df["game_modes"] + " " + df["perspectives"]

    tfidf = TfidfVectorizer(max_features=300)
    X_text = tfidf.fit_transform(df["text_features"])

    X_num = MinMaxScaler().fit_transform(df[["aggregated_rating", "release_year"]].fillna(0))
    game_content_matrix = hstack([X_text, X_num])
    df["game_index"] = df["name"]

    # 2.2 PCA + Clustering pour générer des user_ids
    X_reduced = PCA(n_components=100, random_state=42).fit_transform(X_text.toarray())
    user_ids = MiniBatchKMeans(n_clusters=10, batch_size=1024, random_state=42).fit_predict(X_reduced)
    df["user_id"] = user_ids.astype(str)

    # 2.3 Interactions
    df_lightfm = df[["user_id", "name", "review_score"]].dropna()
    dataset = Dataset()
    dataset.fit(df_lightfm["user_id"], df_lightfm["name"])

    interactions, _ = dataset.build_interactions(
        df_lightfm[["user_id", "name", "review_score"]].values.tolist()
    )
    user_map, _, item_map, _ = dataset.mapping()
    index_to_name = {v: k for k, v in item_map.items()}

    n_items = interactions.shape[1]
    names_ordered = [index_to_name[i] for i in range(n_items)]

    filtered = df.drop_duplicates("name")
    filtered = filtered[filtered["name"].isin(names_ordered)].copy()
    filtered["internal_id"] = filtered["name"].map(item_map).astype(int)
    filtered = filtered.sort_values("internal_id")
    row_indices = filtered.index.to_numpy()
    item_features = game_content_matrix[row_indices]

    model = LightFM(loss="warp")
    model.fit(interactions, item_features=item_features, epochs=10, num_threads=4)

    joblib.dump(model, "modeles_lightfm/lightfm_model_name.pkl")
    joblib.dump({
        "user_map": user_map,
        "item_map": item_map,
        "index_to_name": index_to_name,
        "item_features": item_features
    }, "modeles_lightfm/lightfm_meta_name.pkl")
    print(" Modèle LightFM sauvegardé.")

