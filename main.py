from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from llm_service import generate_report_from_llm

load_dotenv()

app = FastAPI(
    title="1C Audit AI Engine",
    description="Микросервис RAG + LLM для генерации аудиторских заключений 1С",
    version="1.0.0"
)

class AuditRequest(BaseModel):
    doc_ids: str
    vendor_bin: str
    total_amount_kzt: float
    total_amount_mrp: float
    interval_hours: float
    risk_score: float

@app.post("/api/v1/generate-audit-report")
async def generate_audit_report(payload: AuditRequest):
    try:
        data_dict = payload.model_dump()
        report_text = generate_report_from_llm(data_dict)
        return {
            "status": "success",
            "report": report_text
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка обработки: {str(e)}")