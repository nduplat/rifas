from celery import Celery
from .config import settings

celery_app = Celery(
    "rifa1122",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=["app.workers.tasks"]
)

# Celery configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_routes={
        "app.workers.tasks.close_rifa": {"queue": "rifa_operations"},
        "app.workers.tasks.process_payouts": {"queue": "payments"},
        "app.workers.tasks.reconcile_loteria": {"queue": "loteria_sync"},
    },
    beat_schedule={
        "close-expired-rifas": {
            "task": "app.workers.tasks.close_rifa",
            "schedule": 3600.0,  # Every hour
            "args": (),
        },
        "reconcile-loteria-results": {
            "task": "app.workers.tasks.reconcile_loteria",
            "schedule": 1800.0,  # Every 30 minutes
            "args": (),
        },
    },
)

# Optional: Import tasks to ensure they are registered
if __name__ == "__main__":
    celery_app.start()
