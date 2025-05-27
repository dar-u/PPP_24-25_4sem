from fastapi import FastAPI
from app.api.auth import router as auth_router
from app.api.search import router as search_router
from app.db.database import engine, Base

app = FastAPI()
app.include_router(auth_router)
app.include_router(search_router)

@app.on_event("startup")
def startup():
    from app.db.database import engine, Base
    Base.metadata.create_all(bind=engine) 