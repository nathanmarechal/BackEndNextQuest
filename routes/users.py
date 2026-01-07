# users.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from database import get_db
from models.model import User as UserModel
from schemas.schema import User, UserCreate, UserLogin, UserOut
from services.user_service import create_access_token, login_user, create_user_service

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = create_user_service(db, user)
    return db_user

@router.get("/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id_user == user_id).first()
    print(f"Queried user: {user}")
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/", response_model=list[User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(UserModel).offset(skip).limit(limit).all()


@router.post("/login", response_model=dict)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    user = login_user(db, credentials)
    token = create_access_token(data={"sub": str(user.id_user)})
    return {"access_token": token, "token_type": "bearer", "user_id": user.id_user}
