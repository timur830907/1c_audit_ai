import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from llm_service import generate_audit_explanation

app = FastAPI(
    title="1C Audit AI Engine",
    description="Микросервис ИИ-анализа транзакций для 1С:Предприятие",
    version="1.0.0"
)

class AuditRequest(BaseModel):
    doc_ids: str = Field(..., example="PA-20260022, PA-20260023")
    vendor_bin: str = Field(..., example="999111222333")
    total_amount_kzt: float = Field(..., example=1210000.00)
    total_amount_mrp: float = Field(..., example=289.3)
    interval_hours: float = Field(..., example=3.0)
    risk_score: float = Field(..., example=0.94)

@app.get("/")
def read_root():
    return {"status": "ok", "message": "1C Audit AI Engine is running"}

@app.post("/api/v1/generate-audit-report")
async def generate_report(data: AuditRequest):
    try:
        # Для Pydantic v2 используем model_dump() с фоллбэком на dict()
        payload = data.model_dump() if hasattr(data, "model_dump") else data.dict()
        report_text = generate_audit_explanation(payload)
        return {
            "status": "success",
            "risk_score": data.risk_score,
            "report": report_text
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))