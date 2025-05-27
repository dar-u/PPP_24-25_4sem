from celery import Celery
from app.services.fuzzy_search import search_with_levenshtein

celery_app = Celery(
    "worker",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

@celery_app.task
def run_search_task(corpus_text: str, word: str):
    results = []
    words = corpus_text.split()
    for w in set(words):
        dist = search_with_levenshtein(word.lower(), w.lower())
        if dist <= 3:
            results.append({"word": w, "distance": dist})
    return sorted(results, key=lambda x: x["distance"])