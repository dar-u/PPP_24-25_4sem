from sqlalchemy.orm import Session
from app.models.corpus import Corpus
from app.schemas.corpus import CorpusCreate

def upload_corpus(db: Session, corpus: CorpusCreate):
    db_corpus = Corpus(name=corpus.corpus_name, text=corpus.text)
    db.add(db_corpus)
    db.commit()
    db.refresh(db_corpus)
    return {"corpus_id": db_corpus.id, "message": "Corpus uploaded successfully"}

def get_all_corpuses(db: Session):
    return db.query(Corpus).all()