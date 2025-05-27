from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.corpus import CorpusCreate, CorpusOut
from app.cruds.corpus import upload_corpus, get_all_corpuses
from app.services.fuzzy_search import search_with_levenshtein

router = APIRouter(prefix="/search", tags=["Search"])

@router.post("/upload_corpus")
def upload(corpus: CorpusCreate, db: Session = Depends(get_db)):
    return upload_corpus(db, corpus)

@router.get("/corpuses")
def list_corpuses(db: Session = Depends(get_db)):
    corpuses = get_all_corpuses(db)
    return {"corpuses": [{"id": c.id, "name": c.name} for c in corpuses]}

@router.post("/search_algorithm")
def search(word: str, algorithm: str, corpus_id: int, db: Session = Depends(get_db)):
    corpus = db.query(Corpus).get(corpus_id)
    if not corpus:
        raise HTTPException(status_code=404, detail="Corpus not found")

    start_time = time.time()
    if algorithm == "levenshtein":
        results = search_with_levenshtein(corpus.text, word)
    else:
        raise HTTPException(status_code=400, detail="Unsupported algorithm")
    execution_time = time.time() - start_time

    return {
        "execution_time": round(execution_time, 4),
        "results": results
    }

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.corpus import CorpusCreate
from app.cruds.corpus import upload_corpus, get_all_corpuses
from app.services.task_service import start_background_search

router = APIRouter(prefix="/search", tags=["Search"])

#  предыдущие эндпоинты без изменений

@router.post("/start_async_search")
def async_search(word: str, corpus_id: int, db: Session = Depends(get_db)):
    corpus = db.query(Corpus).get(corpus_id)
    if not corpus:
        raise HTTPException(status_code=404, detail="Corpus not found")

    task_id = start_background_search(corpus.text, word)
    return {"task_id": task_id}