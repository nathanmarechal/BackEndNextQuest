from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import users
from routes import recommendation
from routes import games
app = FastAPI()
origins = [
    "http://localhost:5173",  # frontend React
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
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
