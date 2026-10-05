import io
import csv
from fastapi import APIRouter, Body
from fastapi.responses import Response
from typing import List, Dict, Any

router = APIRouter(prefix="/api/export", tags=["export"])

def sanitize_csv_cell(value: Any) -> str:
    """Neutralize spreadsheet formula injection (=, +, -, @)."""
    if value is None:
        return ""
    str_val = str(value)
    if str_val.startswith(("=", "+", "-", "@", "\t", "\r")):
        return "'" + str_val
    return str_val

@router.post("/csv")
async def export_csv(payload: Dict[str, Any] = Body(...)):
    filename = payload.get("filename", "export.csv")
    columns = payload.get("columns", [])
    data = payload.get("data", [])

    output = io.StringIO()
    writer = csv.writer(output)

    # Write headers
    if columns:
        writer.writerow(columns)
    elif data and isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
        columns = list(data[0].keys())
        writer.writerow(columns)

    # Write rows with formula injection sanitization
    for row in data:
        if isinstance(row, dict):
            writer.writerow([sanitize_csv_cell(row.get(col, "")) for col in columns])
        elif isinstance(row, list):
            writer.writerow([sanitize_csv_cell(cell) for cell in row])

    csv_bytes = output.getvalue().encode("utf-8")
    return Response(
        content=csv_bytes,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
