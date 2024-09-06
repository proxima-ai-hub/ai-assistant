from celery import (Celery)
from pipeline import Pipeline


def make_celery(app_name=__name__):
    backend = broker = "redis://localhost:6380/0"
    return Celery(app_name, backend=backend, broker=broker)

celery = make_celery()
pipe = Pipeline()

@celery.task
def generate_text_task(text: str):
    output = pipe.generate(text)
    return output
