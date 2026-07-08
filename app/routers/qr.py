from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import Response
from app.schemas.models import (
    QRGenerateRequest,
    QRGenerateResponse,
    QRGenerateBulkRequest,
    QRGenerateBulkResponse,
)
from app.services.qr_service import QRService

router = APIRouter(tags=["QR Code"])


@router.get("/health")
async def health():
    return {"status": "ok", "version": "1.0.0"}


@router.post("/generate")
async def generate_qr(body: QRGenerateRequest, request: Request):
    try:
        image_bytes = QRService.generate_qr(
            text=body.text,
            size=body.size,
            fg_color=body.color,
            bg_color=body.bg_color,
            logo_b64=body.logo,
            output_format=body.format,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    content_type = "image/png" if body.format == "png" else "image/svg+xml"
    return Response(content=image_bytes, media_type=content_type)


@router.post("/generate/bulk", response_model=QRGenerateBulkResponse)
async def generate_qr_bulk(body: QRGenerateBulkRequest):
    results = []
    for i, item in enumerate(body.items):
        try:
            b64 = QRService.generate_qr_b64(
                text=item.text,
                size=item.size,
                fg_color=item.color,
                bg_color=item.bg_color,
                logo_b64=item.logo,
                output_format=body.format,
            )
            results.append({"index": i, "qr": b64, "error": None})
        except Exception as e:
            results.append({"index": i, "qr": None, "error": str(e)})

    return QRGenerateBulkResponse(success=True, data=results)
