import os
from celery import Celery
from celery.utils.log import get_task_logger

CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")


celery_app = Celery(
    "log_guardian",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
    include=["log_guardian.celery_worker"]
)

task_log = get_task_logger(__name__)

@celery_app.task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={'max_retries': 3}
)
def process_log_file(self, analysis_report_id):
    task_log.info(f"Starting analysis for report ID: {analysis_report_id}")
    #simple placeholder for testing
    import time
    time.sleep(10)
    
    task_log.info(f"Successfully completed analysis for report ID: {analysis_report_id}")
    return f"Report {analysis_report_id} processed."