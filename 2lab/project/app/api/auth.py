
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login/")

from app.api.utils import get_current_user

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate, UserOut
from app.cruds.user import create_user, get_user_by_email
from app.services.auth import authenticate_user
from app.db.session import get_db


router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/sign-up/", response_model=UserOut)
def sign_up(user: UserCreate, db: Session = Depends(get_db)):
    if get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db, user)

@router.post("/login/", response_model=UserOut)
def login(email: str, password: str, db: Session = Depends(get_db)):
    return authenticate_user(db, email, password)

@router.get("/users/me/", response_model=UserOut)
def get_me(current_user: dict = Depends(get_current_user)):
    return current_user




