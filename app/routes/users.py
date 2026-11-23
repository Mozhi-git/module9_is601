from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models import User
from app.schemas import (
    UserCreate,
    UserRead,
    UserLogin,
    UserLoginResponse,
)
from app.security import hash_password, verify_password


router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/register",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
)
def register_user(data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.scalar(
        select(User).where(
            or_(
                User.username == data.username,
                User.email == data.email,
            )
        )
    )

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Username or email already exists",
        )

    user = User(
        username=data.username,
        email=data.email,
        password_hash=hash_password(data.password),
    )

    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Username or email already exists",
        )

    return user


@router.post("/login", response_model=UserLoginResponse)
def login_user(data: UserLogin, db: Session = Depends(get_db)):
    user = db.scalar(
        select(User).where(User.username == data.username)
    )

    if user is None or not verify_password(
        data.password, user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
        )

    return {
        "message": "Login successful",
        "user": user,
    }
