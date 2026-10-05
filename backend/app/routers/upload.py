import json
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Body
from fastapi.responses import PlainTextResponse
from typing import Dict, Any, List
from app.services.upload_service import UploadService, COLUMN_ALIASES, REQUIRED_COLUMNS

router = APIRouter(prefix="/api/upload", tags=["upload"])

@router.post("/preview")
async def preview_upload(
    file: UploadFile = File(...),
    data_type: str = Form("sales")
):
    if not file.filename.lower().endswith((".xlsx", ".xls", ".csv")):
        raise HTTPException(status_code=400, detail="Only Excel (.xlsx/.xls) and CSV (.csv) files are supported.")

    file_bytes = await file.read()
    if len(file_bytes) == 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    try:
        preview_data = UploadService.parse_file_preview(file_bytes, file.filename)
        headers = preview_data["headers"]
        auto_mapping = UploadService.get_auto_mapping(data_type, headers)
        
        return {
            "success": True,
            "filename": file.filename,
            "file_size": len(file_bytes),
            "data_type": data_type,
            "detected_header_row": preview_data["detected_header_row"],
            "headers": headers,
            "preview_rows": preview_data["preview_rows"],
            "suggested_mapping": auto_mapping,
            "required_fields": REQUIRED_COLUMNS.get(data_type, [])
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/validate")
async def validate_upload(
    file: UploadFile = File(...),
    data_type: str = Form("sales"),
    mapping: str = Form(...),  # JSON string
    header_row_idx: int = Form(1)
):
    file_bytes = await file.read()
    try:
        mapping_dict = json.loads(mapping)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON in column mapping parameter.")

    result = await UploadService.validate_and_process(
        file_bytes=file_bytes,
        filename=file.filename,
        data_type=data_type,
        mapping=mapping_dict,
        header_row_idx=header_row_idx
    )
    return result

@router.post("/commit")
async def commit_upload(payload: Dict[str, Any] = Body(...)):
    job_id = payload.get("job_id")
    data_type = payload.get("data_type")
    filename = payload.get("file_name")
    valid_records = payload.get("valid_records", [])
    stats = payload.get("stats", {})

    if not job_id or not data_type:
        raise HTTPException(status_code=400, detail="Missing required job_id or data_type")

    saved_job = await UploadService.commit_import(
        job_id=job_id,
        data_type=data_type,
        filename=filename,
        valid_records=valid_records,
        stats=stats
    )
    return {"success": True, "import_job": saved_job}

@router.get("/history")
async def get_import_history():
    return await UploadService.get_import_history()

@router.get("/template/{data_type}")
async def get_sample_template(data_type: str):
    """Generates clean CSV template with headers and 2 sample rows."""
    templates = {
        "sales": (
            "Bill Date,Store,Item Code,Bill Qty,Selling Price,Net Sales,Gross Sales,Discount Amt,Cogs with GST\n"
            "2026-09-25,CITIMART - CHOWRINGHEE,C880157,4,799.00,3196.00,3196.00,0.00,1520.00\n"
            "2026-09-25,CITIMART - GARIAHAT,C652190,2,1599.00,2878.20,3198.00,319.80,1440.00\n"
        ),
        "inventory": (
            "Snapshot Date,Store,Item Code,Current Stock,Unit Cost,Stock Value,Days in Stock\n"
            "2026-09-30,CITIMART - CHOWRINGHEE,C880157,18,380.00,6840.00,14\n"
            "2026-09-30,CITIMART - GARIAHAT,C661004,85,1650.00,140250.00,165\n"
        ),
        "purchases": (
            "GRC No.,Purchase Date,Store,Vendor,Item Code,Received Qty,Unit Cost,Purchase Value\n"
            "GRC/00000301/26-27,2026-09-15,CITIMART - CHOWRINGHEE,VEND_7144,C880157,120,380.00,45600.00\n"
            "GRC/00000302/26-27,2026-09-18,CITIMART - GARIAHAT,VEND_7170,C652190,50,720.00,36000.00\n"
        ),
        "product_master": (
            "Item Code,Product Name,Division,Section,Department,Category,Brand,Style,Color,Size,Vendor,MRP,Cost Price\n"
            "C880157,Raphaaa Crew Neck T-Shirt Slim,Raphaaa,Mens(R),T-Shirts (Rm),Casual,Raphaaa,Polo,Navy Blue,L,VEND_7144,799.00,380.00\n"
            "C661004,Banarasi Art Silk Zari Saree,Ladies Ethnic,Ethnic Wear,Sarees,Wedding,Mittal,Traditional,Royal Crimson,Free,VEND_6720,3499.00,1650.00\n"
        ),
        "store_master": (
            "Store ID,Store Name,Region,Store Type,Opening Date\n"
            "STR_CHOWRINGHEE,Citimart - Chowringhee,Central Kolkata,Flagship,2018-05-15\n"
            "STR_GARIAHAT,Citimart - Gariahat,South Kolkata,Flagship,2019-09-20\n"
        )
    }

    if data_type not in templates:
        raise HTTPException(status_code=404, detail="Template not found for data type.")

    return PlainTextResponse(
        content=templates[data_type],
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=citimart_{data_type}_template.csv"}
    )
