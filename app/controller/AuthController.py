import datetime
from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.Users import User
from ..models.Role import Role
from ..models.Registration_schema import RegisterRequest, TokenResponse
from ..service.AuthService import (
    get_password_hash,
    verify_password,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
def register_user(request: RegisterRequest, db: Session = Depends(get_db)):
    if len(request.password.encode("utf-8")) > 72:
        raise HTTPException(status_code=400, detail="Password too long (max 72 bytes)")

    user = db.query(User).filter(User.username == request.username).first()
    if user:
        raise HTTPException(status_code=400, detail="Username already registered")

    user_role = db.query(Role).filter(Role.name == "ROLE_USER").first()
    if not user_role:
        raise HTTPException(status_code=500, detail="Default role not found")

    hashed_pw = get_password_hash(request.password)
    new_user = User(
        username=request.username, hashed_password=hashed_pw, roles=[user_role]
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"msg": "User registered successfully"}


@router.post("/login", response_model=TokenResponse)
def login(
    username: str = Form(), password: str = Form(), db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    roles = [role.name for role in user.roles]
    access_token_expires = datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "username": user.username, "roles": roles},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}
