import enum
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    ForeignKey,
    Enum
)
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.dialects.postgresql import JSONB 


DATABASE_URL = "postgresql+psycopg2://log_guardian_user:luka@localhost/log_guardian_db"
engine = create_engine(DATABASE_URL, echo=False)
Base = declarative_base()

class ReportStatus(enum.Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    reports = relationship("AnalysisReport", back_populates="user")
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"

class AnalysisReport(Base):
    __tablename__ = 'analysis_reports'
    id = Column(Integer, primary_key=True)
    status = Column(Enum(ReportStatus), nullable=False, default=ReportStatus.PENDING)
    results = Column(JSONB, nullable=True) 
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship("User", back_populates="reports")
    def __repr__(self):
        return f"<AnalysisReport(id={self.id}, status='{self.status.name}', user_id={self.user_id})>"

if __name__ == '__main__':
    print("Creating database tables for PostgreSQL...")
    Base.metadata.create_all(engine)
    print("Tables created successfully.")