import json
from sqlalchemy.orm import Session
from backend.database import AuditRecordModel

class AnalyticsEngine:

    def __init__(self, db_session: Session):
        self.db = db_session

    def calculate_safety_kpis(self) -> dict:
        records = self.db.query(AuditRecordModel).all()
        if not records:
            return {
                "total_evaluations": 0,
                "passed_count": 0,
                "failed_count": 0,
                "safety_pass_rate": 0.0,
                "average_hallucination_index": 0.0
            }

        total = len(records)
        passed = sum(1 for r in records if r.passed_safety_gate)
        failed = total - passed
        avg_hallucination = sum(r.hallucination_index for r in records) / total

        return {
            "total_evaluations": total,
            "passed_count": passed,
            "failed_count": failed,
            "safety_pass_rate": round((passed / total) * 100, 2),
            "average_hallucination_index": round(avg_hallucination, 4)
        }

    def aggregate_error_distribution(self) -> dict:
        records = self.db.query(AuditRecordModel).all()
        error_counts = {}
        flag_counts = {}

        for r in records:
            try:
                errors = json.loads(r.detected_medical_errors)
                for error in errors:
                    error_counts[error] = error_counts.get(error, 0) + 1
            except Exception:
                pass

            try:
                flags = json.loads(r.critical_red_flags)
                for flag in flags:
                    flag_counts[flag] = flag_counts.get(flag, 0) + 1
            except Exception:
                pass

        return {
            "medical_errors_distribution": error_counts,
            "critical_red_flags_distribution": flag_counts
        }
