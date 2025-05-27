from app.cruds.user import get_user_by_email, create_user
from app.schemas.user import UserCreate
from passlib.context import CryptContext
from jose import jwt
from fastapi import HTTPException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "your-secret-key"

def authenticate_user(db, email, password):
    user = get_user_by_email(db, email)
    if not user or not pwd_context.verify(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = jwt.encode({"id": user.id}, SECRET_KEY, algorithm="HS256")
    user.token = token
    db.commit()
    return user