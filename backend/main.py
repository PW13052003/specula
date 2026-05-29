import json
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import init_db, get_db, AuditRecordModel
from evaluation_engine.evaluator import LocalEvaluationEngine
from evaluation_engine.schemas import ClinicalAuditResult

app = FastAPI(title="Specula API Gateway")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    init_db()

@app.post("/api/evaluate", response_model=ClinicalAuditResult)
def run_evaluation_endpoint(conversation: list, db: Session = Depends(get_db)):
    try:
        engine = LocalEvaluationEngine(model_name="llama3")
        audit_record = engine.evaluate_interaction(conversation)
        
        db_record = AuditRecordModel(
            passed_safety_gate=audit_record.passed_safety_gate,
            hallucination_index=audit_record.hallucination_index,
            critical_red_flags=json.dumps(audit_record.critical_red_flags_identified),
            detected_medical_errors=json.dumps(audit_record.detected_medical_errors),
            severity_assessment_accuracy=audit_record.severity_assessment_accuracy,
            justification_summary=audit_record.justification_summary,
            conversation_log=json.dumps(conversation)
        )
        
        db.add(db_record)
        db.commit()
        db.refresh(db_record)
        
        return audit_record
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
