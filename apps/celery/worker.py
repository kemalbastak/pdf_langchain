from celery import Celery
import os
# Create the Celery app instance
celery_app = Celery(
    "worker",
    broker=os.getenv("REDIS_URL"),
    backend=os.getenv("REDIS_DATABASE_URI"),
)

# Load Celery config (optional, use if you have specific settings)
celery_app.conf.task_routes = {"apps.celery.*": {"queue": "default"}}
celery_app.conf.task_default_queue = "default"

celery_app.autodiscover_tasks(["apps.celery.parser"])

