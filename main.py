from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
import asyncio

from llm_service import generate_audit_explanation

app = FastAPI(
    title="1C Audit AI Microservice",
    description="Микросервис аудита госзакупок РК на предмет искусственного дробления контрактов",
    version="1.0.0"
)

class AuditRequest(BaseModel):
    doc_ids: str
    vendor_bin: str
    total_amount_kzt: float
    total_amount_mrp: float
    interval_hours: float
    risk_score: float

class BatchAuditRequest(BaseModel):
    items: List[AuditRequest]

@app.get("/")
async def root():
    return {"status": "online", "message": "1C Audit AI Microservice is running"}

@app.post("/api/v1/generate-audit-report")
async def audit_endpoint(request: AuditRequest):
    try:
        audit_data = request.model_dump()
        report_text = generate_audit_explanation(audit_data)
        
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

@app.post("/api/v1/generate-batch-report")
async def batch_audit_endpoint(batch_request: BatchAuditRequest):
    try:
        results = []
        for item in batch_request.items:
            audit_data = item.model_dump()
            report_text = generate_audit_explanation(audit_data)
            results.append({
                "doc_ids": item.doc_ids,
                "vendor_bin": item.vendor_bin,
                "risk_score": item.risk_score,
                "report": report_text
            })
            
        return JSONResponse(
            content={
                "status": "success",
                "total_processed": len(results),
                "items": results
            },
            headers={"Content-Type": "application/json; charset=utf-8"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))