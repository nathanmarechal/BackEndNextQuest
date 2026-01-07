import time

from fastapi import FastAPI, Query, HTTPException
import httpx

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import users
from routes import recommendation
from routes import games
from routes import review
from routes.assistant_routes import router as assistant_router

app = FastAPI()
origins = [
    "http://localhost:8080",  # frontend Vite
    "http://127.0.0.1:5173",  # parfois nécessaire aussi
]



app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,          # <- important !
    allow_methods=["*"],
    allow_headers=["*"],
)
import logging
logging.basicConfig(level=logging.DEBUG)

# Include the router from users.py
app.include_router(users.router)
app.include_router(games.router)
app.include_router(recommendation.router)
app.include_router(review.router)
app.include_router(assistant_router)
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


TWITCH_CLIENT_ID = "348xisw17vsxtq23qsp7rsov21pdfh"
TWITCH_ACCESS_TOKEN = "wxm9n25egb5vi8vvuz1nz46ll58hus"

_token_cache = {"value": None, "expires_at": 0}

async def get_app_access_token() -> str:
    if not TWITCH_CLIENT_ID or not TWITCH_ACCESS_TOKEN:
        raise HTTPException(status_code=500, detail="TWITCH_CLIENT_ID / TWITCH_ACCESS_TOKEN manquants")

    # reuse token
    if _token_cache["value"] and time.time() < _token_cache["expires_at"] - 60:
        return _token_cache["value"]

    async with httpx.AsyncClient(timeout=10.0) as client:
        r = await client.post(
            "https://id.twitch.tv/oauth2/token",
            params={
                "client_id": TWITCH_CLIENT_ID,
                "client_secret": TWITCH_ACCESS_TOKEN,
                "grant_type": "client_credentials",
            },
        )
        data = r.json()
        if r.status_code != 200 or "access_token" not in data:
            raise HTTPException(status_code=502, detail={"twitch_token_error": data})

        _token_cache["value"] = data["access_token"]
        _token_cache["expires_at"] = time.time() + int(data.get("expires_in", 0))
        return _token_cache["value"]

@app.get("/twitch/live/{game_name}")
async def get_top_stream(game_name: str):
    token = await get_app_access_token()
    headers = {
        "Client-ID": TWITCH_CLIENT_ID,
        "Authorization": f"Bearer {token}",
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        game_resp = await client.get(
            "https://api.twitch.tv/helix/games",
            params={"name": game_name},
            headers=headers,
        )
        game_data = game_resp.json()

        # si jamais Twitch renvoie un souci auth, on remonte clairement
        if game_resp.status_code == 401:
            raise HTTPException(status_code=502, detail={"twitch_auth_error": game_data})

        if not game_data.get("data"):
            return []  # pas d'erreur: juste pas trouvé côté Twitch

        game_id = game_data["data"][0]["id"]

        streams_resp = await client.get(
            "https://api.twitch.tv/helix/streams",
            params={"game_id": game_id, "first": 5},
            headers=headers,
        )
        streams_data = streams_resp.json()

        if streams_resp.status_code == 401:
            raise HTTPException(status_code=502, detail={"twitch_auth_error": streams_data})

        return streams_data.get("data", [])