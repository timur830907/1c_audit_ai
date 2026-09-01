from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from llm_service import generate_audit_explanation

app = FastAPI(
    title="1C Audit AI Microservice",
    description="Микросервис аудита госзакупок РК на предмет искусственного дробления контрактов",
    version="1.0.0"
)

# Схема входящих данных от 1С / Клиента
class AuditRequest(BaseModel):
    doc_ids: str
    vendor_bin: str
    total_amount_kzt: float
    total_amount_mrp: float
    interval_hours: float
    risk_score: float

@app.get("/")
async def root():
    return {"status": "online", "message": "1C Audit AI Microservice is running"}

@app.post("/api/v1/generate-audit-report")
async def audit_endpoint(request: AuditRequest):
    try:
        # Преобразуем Pydantic-модель в обычный словарь
        audit_data = request.model_dump()
        
        # Генерируем отчет с использованием RAG и Gemini
        report_text = generate_audit_explanation(audit_data)
        
        # Возвращаем JSONResponse с явным указанием UTF-8
        return JSONResponse(
            content={
                "status": "success",
                "risk_score": request.risk_score,
                "report": report_text
            },
            headers={"Content-Type": "application/json; charset=utf-8"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))