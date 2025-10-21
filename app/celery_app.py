from celery import Celery
from celery.schedules import crontab

from app.core.config import get_settings

settings = get_settings()

redis_host = settings.REDIS_HOST or "localhost"
redis_port = settings.REDIS_PORT or 6379
broker_url = f"redis://{redis_host}:{redis_port}/0"

app = Celery("katana_link", broker=broker_url)

app.autodiscover_tasks(["app.tasks"])

app.conf.beat_schedule = {
    "write-back-visits-every-five-minutes": {
        "task": "app.tasks.counter_tasks.write_back_visits_to_db",
        "schedule": crontab(minute="*/5"),
    }
}

app.conf.timezone = "UTC"
