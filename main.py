import traceback
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from llm_service import generate_audit_explanation

app = FastAPI(
    title="1C Audit AI Engine",
    version="1.0.0",
    description="Микросервис ИИ-анализа транзакций для 1С:Предприятие"
)


class AuditRequest(BaseModel):
    doc_ids: str
    vendor_bin: str
    total_amount_kzt: float
    total_amount_mrp: float
    interval_hours: float
    risk_score: float


@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": "1C Audit AI Engine",
        "version": "1.0.0"
    }


@app.post("/api/v1/generate-audit-report")
async def generate_report(data: AuditRequest):
    try:
        payload = data.model_dump() if hasattr(data, "model_dump") else data.dict()
        report_text = generate_audit_explanation(payload)
        
        return {
            "status": "success",
            "risk_score": data.risk_score,
            "report": report_text
        }
    except Exception as e:
        error_trace = traceback.format_exc()
        print("=== ERROR IN AUDIT REPORT GENERATION ===")
        print(error_trace)
        print("========================================")
        raise HTTPException(
            status_code=500,
            detail=f"Internal Server Error: {str(e)}"
        )