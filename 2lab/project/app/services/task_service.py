
from app.tasks.search_tasks import run_search_task

def start_background_search(corpus_text: str, word: str):
    task = run_search_task.delay(corpus_text, word)
    return task.id