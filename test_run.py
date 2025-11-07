import os
import time
from sqlalchemy.orm import Session

from log_guardian.celery_worker import process_log_file
from log_guardian.database import SessionLocal
from log_guardian.models import User, AnalysisReport, ReportStatus

def main():

    print("--- [Step 1/4] Setting up test data in the database ---")
    
    db: Session = SessionLocal()
    
    try:

        test_user = db.query(User).filter(User.username == "testuser").first()
        if not test_user:
            print("Creating a new test user...")
            test_user = User(username="testuser", password_hash="fake_hash")
            db.add(test_user)
            db.commit()
            db.refresh(test_user)
        
        print(f"Using user: {test_user.username} (ID: {test_user.id})")

        print("Creating a new analysis report with PENDING status...")
        new_report = AnalysisReport(
            user_id=test_user.id,
            status=ReportStatus.PENDING,
            results={} 
        )
        db.add(new_report)
        db.commit()
        db.refresh(new_report)
        
        report_id = new_report.id
        print(f"Successfully created report with ID: {report_id}")

        file_to_process = os.path.join(os.path.dirname(__file__), 'log.log')
        print(f"File to process: {file_to_process}")

        print("\n--- [Step 2/4] Dispatching Celery task ---")
        
        task = process_log_file.delay(analysis_report_id=report_id, file_path=file_to_process)
        print(f"Task dispatched successfully! Task ID: {task.id}")
        
        print("\n--- [Step 3/4] Waiting for task completion ---")

        result = task.get(timeout=30)
        print(f"Task completed with result: '{result}'")

        print("\n--- [Step 4/4] Verifying results in the database ---")
        
        db.expire(new_report)
        
        verified_report = db.query(AnalysisReport).filter(AnalysisReport.id == report_id).first()
        
        print(f"Final Report Status: {verified_report.status.name}")
        print(f"Final Report Results: {verified_report.results}")

        if verified_report.status == ReportStatus.COMPLETED:
            print("\n✅ SUCCESS: The pipeline completed successfully!")
        else:
            print("\n❌ FAILED: The report status was not updated to COMPLETED.")

    except Exception as e:
        print(f"\nAn error occurred: {e}")
        db.rollback()
    finally:
        print("\nClosing database session.")
        db.close()


if __name__ == "__main__":
    main()