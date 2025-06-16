from celery import Celery

from app.core.config import settings


celery_app = Celery(
    "celery_app",
    broker=settings.CELERY_BROKER_URL
)

celery_app.conf.task_routes = {
    "tasks.rag.process_document": {
        'queue': 'rag'
    }
}
