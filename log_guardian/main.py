import os
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from . import models
from .database import engine, get_db_session
from .celery_worker import process_log_file

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="LogGuardian API",
    description="An API to trigger and manage security log analysis.",
    version="1.0.0"
)


class ReportRequest(BaseModel):
    file_path: str = Field(..., example="/path/to/your/logFile.log")

class ReportResponse(BaseModel):
    report_id: int
    status: str
    message: str


@app.post("/api/reports", response_model=ReportResponse, status_code=status.HTTP_202_ACCEPTED)
async def create_analysis_report(request: ReportRequest, db: Session = Depends(get_db_session)):
    USER_ID_FOR_DEMO = 1
    
    if not os.path.exists(request.file_path):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File not found: {request.file_path}"
        )

    new_report = models.AnalysisReport(
        user_id=USER_ID_FOR_DEMO,
        status=models.ReportStatus.PENDING
    )
    db.add(new_report)
    db.commit()
    db.refresh(new_report)

    process_log_file.delay(analysis_report_id=new_report.id, file_path=request.file_path)

    return {
        "report_id": new_report.id,
        "status": new_report.status.name,
        "message": "Analysis task has been accepted and is scheduled for processing."
    }