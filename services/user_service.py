from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import HTTPException
from models.model import User
from schemas.schema import UserCreate, UserLogin
from sqlalchemy.orm import Session
import bcrypt

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


def create_user_service(db: Session, user: UserCreate):
    print(f"[DEBUG] Création de l'utilisateur : {user.username}, email : {user.email}")
    existing = db.query(User).filter(User.email_user == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    db_user = User(
        name_user=user.username,
        password=hash_password(user.password),
        email_user=user.email,
        date_of_birth=user.birthdate
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

def login_user(db: Session, credentials: UserLogin):
    user = db.query(User).filter(User.email_user == credentials.email).first()
    if not user or not verify_password(credentials.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return user

