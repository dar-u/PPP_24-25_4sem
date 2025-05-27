from pydantic import BaseModel

class CorpusCreate(BaseModel):
    corpus_name: str
    text: str

class CorpusOut(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True