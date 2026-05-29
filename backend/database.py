import os
from sqlalchemy import create_engine, Column, Integer, Boolean, Float, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./specula.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class AuditRecordModel(Base):
    __tablename__ = "audit_records"

    id = Column(Integer, primary_key=True, index=True)
    passed_safety_gate = Column(Boolean, nullable=False)
    hallucination_index = Column(Float, nullable=False)
    critical_red_flags = Column(Text, nullable=False)
    detected_medical_errors = Column(Text, nullable=False)
    severity_assessment_accuracy = Column(String, nullable=False)
    justification_summary = Column(Text, nullable=False)
    conversation_log = Column(Text, nullable=False)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
