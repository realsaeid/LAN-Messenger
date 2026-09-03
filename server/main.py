from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .models import User
from .schemas import UserLogin, UserRegister, UserResponse
from .auth import hash_password, verify_password


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="LAN Messenger",
    description="Local Network Messaging Server",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "LAN Messenger Server is running!"
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }


@app.post("/register", response_model=UserResponse)
def register(
    user: UserRegister,
    db: Session = Depends(get_db)
):

    existing_user = (
        db.query(User)
        .filter(User.username == user.username)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    new_user = User(
        username=user.username,
        password_hash=hash_password(user.password),
        full_name=user.full_name
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.post("/login")
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):

    existing_user = (
        db.query(User)
        .filter(User.username == user.username)
        .first()
    )

    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    if not verify_password(
        user.password,
        existing_user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    existing_user.is_online = True
    db.commit()

    return {
        "message": "Login successful",
        "username": existing_user.username
    }


@app.get("/users", response_model=list[UserResponse])
def get_users(
    db: Session = Depends(get_db)
):

    return db.query(User).all()