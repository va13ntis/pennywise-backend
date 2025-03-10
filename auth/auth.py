from fastapi import APIRouter, HTTPException, Depends
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt

SECRET_KEY = "your_secret_key"  # Change this in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter()

# Fake in-memory database
fake_users_db = {}


def get_password_hash(password):
    return pwd_context.hash(password)


@router.post("/register")
def register_user(email: str, password: str):
    if email in fake_users_db:
        raise HTTPException(status_code=400, detail="Email already registered")
    fake_users_db[email] = get_password_hash(password)
    return {"message": "User registered successfully"}


@router.post("/login")
def login(email: str, password: str):
    user = fake_users_db.get(email)
    if not user or not pwd_context.verify(password, user):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = jwt.encode({"sub": email, "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)},
                              SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": access_token, "token_type": "bearer"}
