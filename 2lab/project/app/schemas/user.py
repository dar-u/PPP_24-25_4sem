from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    password: str

class UserOut(BaseModel):
    id: int
    email: str
    token: str = None

    class Config:
        orm_mode = True