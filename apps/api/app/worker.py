from celery import Celery
from .core.config import settings

celery_app = Celery("resume_ai", broker=settings.redis_url, backend=settings.redis_url)
celery_app.conf.update(task_serializer="json", result_serializer="json", accept_content=["json"], timezone="UTC", task_track_started=True)

@celery_app.task(name="resume_ai.healthcheck")
def healthcheck():
    return {"status": "ok"}
