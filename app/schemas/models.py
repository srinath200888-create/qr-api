from pydantic import BaseModel, Field
from typing import Optional


class QRGenerateRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=2000)
    size: int = Field(200, ge=50, le=4096)
    color: str = Field("#000000", pattern=r"^#[0-9a-fA-F]{6}$")
    bg_color: str = Field("#FFFFFF", pattern=r"^#[0-9a-fA-F]{6}$")
    format: str = Field("png", pattern=r"^(png|svg)$")
    logo: Optional[str] = Field(None)


class QRGenerateResponse(BaseModel):
    success: bool
    error: Optional[str] = None


class QRGenerateBulkItem(BaseModel):
    text: str = Field(..., min_length=1, max_length=2000)
    size: int = Field(200, ge=50, le=4096)
    color: str = Field("#000000", pattern=r"^#[0-9a-fA-F]{6}$")
    bg_color: str = Field("#FFFFFF", pattern=r"^#[0-9a-fA-F]{6}$")
    logo: Optional[str] = None


class QRGenerateBulkRequest(BaseModel):
    items: list[QRGenerateBulkItem] = Field(..., min_length=1, max_length=100)
    format: str = Field("png", pattern=r"^(png|svg)$")


class QRGenerateBulkResponse(BaseModel):
    success: bool
    data: list[dict]
    error: Optional[str] = None
