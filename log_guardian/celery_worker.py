import os
import time
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from celery import Celery
from celery.utils.log import get_task_logger

from .database import SessionLocal
from .models import AnalysisReport, ReportStatus
from .parser import parse_log_file
from .config import settings
from .analysis import analyze_log_data 


celery_app = Celery(
    "log_guardian",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["log_guardian.celery_worker"]
)

task_log = get_task_logger(__name__)

@celery_app.task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={'max_retries': 3},
    name='tasks.process_log_file'
)
def process_log_file(self, analysis_report_id: int, file_path: str):
    task_log.info(f"Starting analysis for report ID: {analysis_report_id} | File: {file_path}")

    db = SessionLocal()
    report = None 
    try:
        report = db.query(AnalysisReport).filter(AnalysisReport.id == analysis_report_id).first()
        if not report:
            task_log.error(f"AnalysisReport with ID {analysis_report_id} not found.")
            return

        report.status = ReportStatus.PROCESSING
        db.commit()

        parsed_data = list(parse_log_file(file_path))
        analysis_results = analyze_log_data(parsed_data)
        report.results = analysis_results
        report.status = ReportStatus.COMPLETED
        db.commit()
                
        task_log.info(f"Successfully completed analysis for report ID: {analysis_report_id}")
        return f"Report {analysis_report_id} processed. Found {analysis_results['suspicious_entries_found']} suspicious entries."
    
    except Exception as e:
        task_log.error(f"Analysis failed for report ID {analysis_report_id}: {e}", exc_info=True)
        
        if report:
            db.rollback()
            report.status = ReportStatus.FAILED
            report.results = {"error": str(e)}
            db.commit()

        raise

    finally:
        db.close()