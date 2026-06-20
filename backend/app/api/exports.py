from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Dict
from app.services.export_service import ExportService
from app.core.logging import logger

router = APIRouter(prefix="/exports", tags=["exports"])


class ExportCSVRequest(BaseModel):
    data: List[Dict]
    filename: str = "export.csv"


class ExportExcelRequest(BaseModel):
    data: List[Dict]
    filename: str = "export.xlsx"


class ExportPDFRequest(BaseModel):
    data: List[Dict]
    question: str
    sql: str
    insight: str
    filename: str = "report.pdf"


@router.post("/csv")
async def export_csv(request: ExportCSVRequest):
    try:
        service = ExportService()
        output, filename = service.export_csv(request.data, request.filename)
        return StreamingResponse(
            output,
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except Exception as e:
        logger.error(f"CSV export failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to export CSV")


@router.post("/excel")
async def export_excel(request: ExportExcelRequest):
    try:
        service = ExportService()
        output, filename = service.export_excel(request.data, request.filename)
        return StreamingResponse(
            output,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except Exception as e:
        logger.error(f"Excel export failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to export Excel")


@router.post("/pdf")
async def export_pdf(request: ExportPDFRequest):
    try:
        service = ExportService()
        output, filename = service.export_pdf(
            request.data,
            request.question,
            request.sql,
            request.insight,
            request.filename
        )
        return StreamingResponse(
            output,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except Exception as e:
        logger.error(f"PDF export failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to export PDF")
