from pydantic_core.core_schema import DateSchema
from sqlalchemy import Column, Boolean, Integer, String, Text, ForeignKey, Table
from sqlalchemy.types import Date
from sqlalchemy.orm import relationship
from database import Base

# === Table de liaison ===

class GenreGame(Base):
    __tablename__ = "genres_games"
    app_id = Column(Integer, ForeignKey("games.app_id"), primary_key=True)
    id_genre = Column(Integer, ForeignKey("genres.id_genre"), primary_key=True)

class PlatformGame(Base):
    __tablename__ = "platforms_games"
    app_id = Column(Integer, ForeignKey("games.app_id"), primary_key=True)
    id_platform = Column(Integer, ForeignKey("platforms.id_platform"), primary_key=True)

class GameModeGame(Base):
    __tablename__ = "game_modes_games"
    app_id = Column(Integer, ForeignKey("games.app_id"), primary_key=True)
    Id_Game_mode = Column(Integer, ForeignKey("game_modes.Id_Game_mode"), primary_key=True)

class ThemeGame(Base):
    __tablename__ = "themes_games"
    app_id = Column(Integer, ForeignKey("games.app_id"), primary_key=True)
    id_theme = Column(Integer, ForeignKey("themes.id_theme"), primary_key=True)

class PerspectiveGame(Base):
    __tablename__ = "perspectives_games"
    app_id = Column(Integer, ForeignKey("games.app_id"), primary_key=True)
    id_perspective = Column(Integer, ForeignKey("perspectives.id_perspective"), primary_key=True)

# === Entités principales ===

class User(Base):
    __tablename__ = "users"

    id_user = Column(Integer, primary_key=True, index=True)
    password = Column(String(100), nullable=False)
    name_user = Column(String(250), nullable=False)
    email_user = Column(String(250), nullable=False)
    date_of_birth = Column(Date)

    reviews = relationship("Review", back_populates="user")
    likes = relationship("IsLiked", back_populates="user")

class Genre(Base):
    __tablename__ = "genres"
    id_genre = Column(Integer, primary_key=True, index=True)
    name_genre = Column(String(500))

    games = relationship("Game", secondary="genres_games", back_populates="genres")

class Platform(Base):
    __tablename__ = "platforms"
    id_platform = Column(Integer, primary_key=True, index=True)
    nom_platform = Column(String(500))

    games = relationship("Game", secondary="platforms_games", back_populates="platforms")

class GameMode(Base):
    __tablename__ = "game_modes"
    Id_Game_mode = Column(Integer, primary_key=True, index=True)
    nom_game_mode = Column(String(500))

    games = relationship("Game", secondary="game_modes_games", back_populates="game_modes")

class Theme(Base):
    __tablename__ = "themes"
    id_theme = Column(Integer, primary_key=True, index=True)
    nom_theme = Column(String(500))

    games = relationship("Game", secondary="themes_games", back_populates="themes")

class Perspective(Base):
    __tablename__ = "perspectives"
    id_perspective = Column(Integer, primary_key=True, index=True)
    nom_perspective = Column(String(50))

    games = relationship("Game", secondary="perspectives_games", back_populates="perspectives")

class Developer(Base):
    __tablename__ = "developers"
    id_developer = Column(Integer, primary_key=True, index=True)
    name_developer = Column(Text)

    games = relationship("Game", back_populates="developer")

class Game(Base):
    __tablename__ = "games"
    app_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    game_summary = Column(Text)
    storyline = Column(Text)
    cover_url = Column(Text)
    artwork_url = Column(Text)
    website = Column(Text)
    id_developer = Column(Integer, ForeignKey("developers.id_developer"))

    developer = relationship("Developer", back_populates="games")
    reviews = relationship("Review", back_populates="game")
    likes = relationship("IsLiked", back_populates="game")

    genres = relationship("Genre", secondary="genres_games", back_populates="games")
    platforms = relationship("Platform", secondary="platforms_games", back_populates="games")
    game_modes = relationship("GameMode", secondary="game_modes_games", back_populates="games")
    themes = relationship("Theme", secondary="themes_games", back_populates="games")
    perspectives = relationship("Perspective", secondary="perspectives_games", back_populates="games")

class Review(Base):
    __tablename__ = "review"
    id_user = Column(Integer, ForeignKey("users.id_user"), primary_key=True)
    app_id = Column(Integer, ForeignKey("games.app_id"), primary_key=True)
    review = Column(String(200))
    review_score = Column(Integer)
    date_review = Column(Date)

    user = relationship("User", back_populates="reviews")
    game = relationship("Game", back_populates="reviews")

class IsLiked(Base):
    __tablename__ = "isliked"

    id_user = Column(Integer, ForeignKey("users.id_user"), primary_key=True)
    app_id = Column(Integer, ForeignKey("games.app_id"), primary_key=True)
    isliked_value = Column(Boolean, nullable=False)

    user = relationship("User", back_populates="likes")
    game = relationship("Game", back_populates="likes")