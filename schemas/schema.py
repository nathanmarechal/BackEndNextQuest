from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import date

class User(BaseModel):
    id_user: int
    name_user: str
    email_user: EmailStr
    age_user: Optional[int] = None

    class Config:
        from_attributes = True

class UserCreate(User):
    password: str

class User(User):
    id_user: int

    class Config:
        orm_mode = True

class ReviewBase(BaseModel):
    review: Optional[str] = None
    review_score: int
    date_review: Optional[date] = None

class ReviewCreate(ReviewBase):
    id_user: int
    app_id: int

class Review(ReviewBase):
    id_user: int
    app_id: int

    class Config:
        orm_mode = True

class Game(BaseModel):
    app_id: int
    name: str
    game_summary: str | None = None
    storyline: str | None = None
    cover_url: str | None = None
    artwork_url: str | None = None
    website: str | None = None

    class Config:
        from_attributes = True

class GameReviewRequest(BaseModel):
    game_name: str
    offset: int = 0
    limit: int = 5

class ReviewWithUserName(BaseModel):
    id_user: int
    app_id: int
    review: Optional[str] = None
    review_score: int
    date_review: Optional[date] = None
    user_name: str

    class Config:
        orm_mode = True

class GameListRequest(BaseModel):
    offset: int = 0
    limit: int = 10
    order_by_name: Optional[bool] = False
    genre: Optional[List[str]] = None
    platform: Optional[List[str]] = None
    developer: Optional[List[str]] = None
    perspective: Optional[List[str]] = None
    game_mode: Optional[List[str]] = None
    theme: Optional[List[str]] = None
    name: Optional[str] = None