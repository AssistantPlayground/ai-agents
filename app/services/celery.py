from app.core.celery import celery_app


@celery_app.task
def process_document(document_url: str, metadata: dict):
    print(f"Processing document {document_url}")
