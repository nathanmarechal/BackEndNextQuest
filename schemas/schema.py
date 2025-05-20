from pydantic import BaseModel, EmailStr
from typing import Optional
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
