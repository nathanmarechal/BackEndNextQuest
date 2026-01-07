from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import date

class User(BaseModel):
    id_user: int
    name_user: str
    email_user: EmailStr
    birthdate: date = None

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    birthdate: date

    class Config:
        from_attributes = True

class UserOut(BaseModel):
    id_user: int
    name_user: str
    email_user: EmailStr
    date_of_birth: date

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str

    class Config:
        from_attributes = True


class ReviewBase(BaseModel):
    review: Optional[str] = None
    review_score: int
    date_review: Optional[date] = None

class ReviewCreate(BaseModel):
    id_user: int
    app_id: int
    review: str
    review_score: float
    date_review: str
    name_user: str

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

class LikeRequest(BaseModel):
    user_id: int
    app_id: int
    liked: bool

class AssistantChatRequest(BaseModel):
    message: str
    gameTitle: Optional[str] = None
    conversationId: Optional[str] = None

class AssistantChatResponse(BaseModel):
    reply: str
    conversationId: Optional[str] = None