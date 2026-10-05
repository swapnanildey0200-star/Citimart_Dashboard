import io
import csv
import re
import uuid
from datetime import datetime, date
from typing import Dict, Any, List, Optional, Tuple
import pandas as pd
import openpyxl
from app.database import db_manager

# Standard column aliases for auto-mapping
COLUMN_ALIASES = {
    "sales": {
        "date": ["bill date", "date", "sale date", "bill_date", "invoice date", "trans date"],
        "store_id": ["store", "store id", "store name", "store_id", "branch", "shop", "location"],
        "sku": ["item code", "itemcode", "sku", "barcode", "product code", "item_code", "product id"],
        "quantity": ["sum of bill qty", "bill qty", "qty", "quantity", "sold qty", "net qty"],
        "selling_price": ["mrp", "std rate", "selling price", "rate", "price"],
        "net_sales": ["sum of net amt", "net sales", "net amt", "net amount", "total amount", "sale value"],
        "gross_sales": ["gross sales", "gross amt", "mrp value", "gross amount"],
        "discount": ["sum of discount amt", "discount amt", "discount", "promo amt", "sum of promo amt"],
        "cogs": ["sum of cogs with gst", "cogs", "cost", "cost price", "std cost"]
    },
    "inventory": {
        "snapshot_date": ["snapshot date", "date", "as on date", "stock date"],
        "store_id": ["store", "store id", "store name", "store_id", "location"],
        "sku": ["item code", "sku", "barcode", "item_code", "product code"],
        "stock_qty": ["stock qty", "closing stock", "current stock", "stock quantity", "qty", "all stors stock"],
        "unit_cost": ["unit cost", "cost price", "cost", "std rate"],
        "stock_value": ["stock value", "stock val", "total cost", "inventory value"],
        "age_days": ["ageing", "age days", "days in stock", "age"]
    },
    "purchases": {
        "po_id": ["grc no.", "grc no", "po id", "po number", "invoice no", "po_id"],
        "date": ["purchase date", "receive date", "date", "grc date"],
        "store_id": ["store", "store id", "store name", "store_id", "location"],
        "vendor_id": ["vendor", "vendor id", "supplier", "vendor name"],
        "sku": ["item code", "sku", "barcode", "product code"],
        "quantity": ["qty", "received qty", "quantity", "purchase qty"],
        "unit_cost": ["unit cost", "std rate", "rate", "cost"],
        "purchase_value": ["purchase value", "total value", "amount", "net amount"]
    },
    "product_master": {
        "sku": ["item code", "sku", "product id", "barcode", "item_code"],
        "name": ["product name", "description", "item name", "item description"],
        "division": ["division", "div"],
        "section": ["section", "sec"],
        "department": ["department", "dept"],
        "category": ["category", "catagory - 1", "cat-1", "cat"],
        "brand": ["brand", "cat-2 (brand)", "cat-2"],
        "style": ["style", "cat-1 (design no.)", "design no"],
        "color": ["color", "colour"],
        "size": ["size", "cat-5 (size)"],
        "vendor_id": ["vendor", "vendor id", "supplier"],
        "mrp": ["mrp", "rsp", "retail price", "selling price"],
        "cost_price": ["cost price", "cost", "std rate", "unit cost"]
    },
    "store_master": {
        "store_id": ["store id", "store code", "store_id", "id"],
        "name": ["store name", "name", "store"],
        "region": ["region", "zone", "city", "location"],
        "store_type": ["store type", "type", "format"],
        "opening_date": ["opening date", "launch date", "open date"]
    }
}

REQUIRED_COLUMNS = {
    "sales": ["date", "store_id", "sku", "quantity", "net_sales"],
    "inventory": ["store_id", "sku", "stock_qty"],
    "purchases": ["date", "store_id", "sku", "quantity", "unit_cost"],
    "product_master": ["sku", "name", "division", "department"],
    "store_master": ["store_id", "name"]
}

class UploadService:
    @staticmethod
    def parse_file_preview(file_bytes: bytes, filename: str) -> Dict[str, Any]:
        """Reads file, locates header row, returns all headers, and provides 10 preview rows."""
        is_excel = filename.lower().endswith((".xlsx", ".xls"))
        
        try:
            if is_excel:
                # Open with openpyxl to scan first 10 rows for actual header
                wb = openpyxl.load_workbook(io.BytesIO(file_bytes), read_only=True, data_only=True)
                sheet = wb.active
                raw_rows = []
                for row in sheet.iter_rows(values_only=True):
                    raw_rows.append([str(c) if c is not None else "" for c in row])
                    if len(raw_rows) >= 20:
                        break
                wb.close()
            else:
                # CSV
                content = file_bytes.decode("utf-8", errors="replace")
                reader = csv.reader(io.StringIO(content))
                raw_rows = []
                for row in reader:
                    raw_rows.append(row)
                    if len(raw_rows) >= 20:
                        break
        except Exception as e:
            raise ValueError(f"Unable to read file: {e}")

        if not raw_rows:
            raise ValueError("The uploaded file is completely empty.")

        # Header detection: find row with highest number of non-empty string headers
        best_header_idx = 0
        max_headers = 0
        for idx, row in enumerate(raw_rows[:8]):
            valid_headers = [c.strip() for c in row if c and c.strip()]
            if len(valid_headers) > max_headers:
                max_headers = len(valid_headers)
                best_header_idx = idx

        headers = [h.strip() for h in raw_rows[best_header_idx]]
        preview_data = []
        for r in raw_rows[best_header_idx + 1: best_header_idx + 11]:
            # pad or slice to match headers length
            padded = (r + [""] * len(headers))[:len(headers)]
            preview_data.append(padded)

        return {
            "filename": filename,
            "detected_header_row": best_header_idx + 1,
            "headers": headers,
            "preview_rows": preview_data,
            "total_preview_count": len(preview_data)
        }

    @staticmethod
    def get_auto_mapping(data_type: str, headers: List[str]) -> Dict[str, Optional[str]]:
        """Suggests mapping from file headers to target schema fields."""
        target_fields = COLUMN_ALIASES.get(data_type, {})
        mapping: Dict[str, Optional[str]] = {}

        for target_field, aliases in target_fields.items():
            matched_header = None
            for h in headers:
                clean_h = h.lower().strip()
                # exact or alias match
                if clean_h == target_field.lower():
                    matched_header = h
                    break
                for alias in aliases:
                    if alias in clean_h or clean_h in alias:
                        matched_header = h
                        break
                if matched_header:
                    break
            mapping[target_field] = matched_header

        return mapping

    @staticmethod
    async def validate_and_process(
        file_bytes: bytes,
        filename: str,
        data_type: str,
        mapping: Dict[str, str],
        header_row_idx: int = 1
    ) -> Dict[str, Any]:
        """Validates all rows, detects errors and duplicates, and prepares valid records."""
        is_excel = filename.lower().endswith((".xlsx", ".xls"))
        job_id = f"JOB_{uuid.uuid4().hex[:10].upper()}"

        # Load reference masters for foreign key validation
        stores_coll = db_manager.get_collection("stores")
        products_coll = db_manager.get_collection("products")
        vendors_coll = db_manager.get_collection("vendors")

        known_stores = {s["store_id"]: s for s in await stores_coll.find({})}
        # also match store by name lower
        store_name_to_id = {s["name"].lower(): s["store_id"] for s in known_stores.values()}

        known_products = {p["sku"]: p for p in await products_coll.find({})}
        known_vendors = {v["vendor_id"]: v for v in await vendors_coll.find({})}

        # Read entire file into pandas dataframe
        skip = max(0, header_row_idx - 1)
        if is_excel:
            df = pd.read_excel(io.BytesIO(file_bytes), skiprows=skip)
        else:
            df = pd.read_csv(io.BytesIO(file_bytes), skiprows=skip)

        total_rows = len(df)
        valid_records = []
        errors = []
        warnings = []
        duplicate_count = 0
        seen_keys = set()

        req_cols = REQUIRED_COLUMNS.get(data_type, [])
        # Check if mapped required columns are present in mapping
        for rc in req_cols:
            if not mapping.get(rc) or mapping[rc] not in df.columns:
                errors.append({
                    "row_number": 0,
                    "field": rc,
                    "value": None,
                    "reason": f"Required field '{rc}' is not mapped to any column in the uploaded file.",
                    "severity": "error"
                })

        if errors:
            return {
                "job_id": job_id,
                "data_type": data_type,
                "file_name": filename,
                "total_rows": total_rows,
                "valid_rows": 0,
                "invalid_rows": total_rows,
                "duplicate_rows": 0,
                "warning_count": 0,
                "status": "failed",
                "errors": errors[:100],
                "valid_records": []
            }

        # Validate rows one by one
        for row_idx, row in df.iterrows():
            current_row_num = row_idx + header_row_idx + 1
            row_errors = []
            record: Dict[str, Any] = {"import_job_id": job_id}

            # Map fields
            for target_field, mapped_col in mapping.items():
                if mapped_col and mapped_col in df.columns:
                    val = row[mapped_col]
                    record[target_field] = val if pd.notna(val) else None
                else:
                    record[target_field] = None

            # Validation logic by data type
            if data_type == "sales":
                # Date check
                dt_val = record.get("date")
                parsed_date = None
                if dt_val is None:
                    row_errors.append("Missing transaction date")
                elif isinstance(dt_val, (datetime, date)):
                    parsed_date = dt_val.strftime("%Y-%m-%d")
                elif isinstance(dt_val, (int, float)) and dt_val > 40000:
                    # Excel serial date
                    parsed_date = (datetime(1899, 12, 30) + pd.to_timedelta(dt_val, unit='D')).strftime("%Y-%m-%d")
                else:
                    try:
                        parsed_date = pd.to_datetime(dt_val).strftime("%Y-%m-%d")
                    except Exception:
                        row_errors.append(f"Invalid date format: {dt_val}")

                record["date"] = parsed_date

                # Store matching
                store_val = str(record.get("store_id") or "").strip()
                if not store_val:
                    row_errors.append("Missing store identifier")
                else:
                    if store_val in known_stores:
                        record["store_id"] = store_val
                    elif store_val.lower() in store_name_to_id:
                        record["store_id"] = store_name_to_id[store_val.lower()]
                    else:
                        # Auto-create or flag unknown
                        warnings.append({
                            "row_number": current_row_num,
                            "field": "store_id",
                            "value": store_val,
                            "reason": f"Store '{store_val}' not found in Store Master. Will auto-register.",
                            "severity": "warning"
                        })
                        record["store_id"] = store_val

                # SKU check
                sku_val = str(record.get("sku") or "").strip()
                if not sku_val or sku_val == "nan":
                    row_errors.append("Missing SKU / Item Code")
                else:
                    record["sku"] = sku_val
                    if sku_val not in known_products:
                        warnings.append({
                            "row_number": current_row_num,
                            "field": "sku",
                            "value": sku_val,
                            "reason": f"SKU '{sku_val}' not found in Product Master.",
                            "severity": "warning"
                        })

                # Quantity check
                try:
                    qty = float(record.get("quantity") or 0)
                    if qty < 0:
                        row_errors.append(f"Negative sales quantity: {qty}")
                    record["quantity"] = qty
                except Exception:
                    row_errors.append(f"Invalid quantity: {record.get('quantity')}")

                # Net sales
                try:
                    net_sales = float(record.get("net_sales") or 0)
                    record["net_sales"] = net_sales
                except Exception:
                    row_errors.append(f"Invalid net sales amount: {record.get('net_sales')}")

                # Selling price / MRP
                try:
                    record["selling_price"] = float(record.get("selling_price") or record.get("mrp") or 0.0)
                except Exception:
                    record["selling_price"] = 0.0

                # COGS / Gross / Discount
                try:
                    record["cogs"] = float(record.get("cogs") or 0.0)
                    record["gross_sales"] = float(record.get("gross_sales") or record["net_sales"])
                    record["discount"] = float(record.get("discount") or 0.0)
                except Exception:
                    pass

                # Period type (TY vs LY based on date year)
                if parsed_date:
                    record["period_type"] = "TY" if parsed_date.startswith("2026") else "LY"
                else:
                    record["period_type"] = "TY"

                # Duplicate transaction detection
                tx_key = f"{record.get('date')}_{record.get('store_id')}_{record.get('sku')}_{record.get('quantity')}"
                if tx_key in seen_keys:
                    duplicate_count += 1
                    row_errors.append("Duplicate transaction row detected in file.")
                else:
                    seen_keys.add(tx_key)

                record["transaction_id"] = f"TX_IMP_{uuid.uuid4().hex[:8]}"
                record["is_void"] = False

            elif data_type == "inventory":
                sku_val = str(record.get("sku") or "").strip()
                store_val = str(record.get("store_id") or "").strip()
                if not sku_val or sku_val == "nan":
                    row_errors.append("Missing SKU")
                if not store_val or store_val == "nan":
                    row_errors.append("Missing Store ID")

                try:
                    record["stock_qty"] = float(record.get("stock_qty") or 0)
                    record["unit_cost"] = float(record.get("unit_cost") or 0)
                    record["stock_value"] = float(record.get("stock_value") or (record["stock_qty"] * record["unit_cost"]))
                    record["age_days"] = int(record.get("age_days") or 15)
                except Exception as e:
                    row_errors.append(f"Numeric parse error: {e}")

                record["snapshot_date"] = record.get("snapshot_date") or datetime.utcnow().strftime("%Y-%m-%d")

            elif data_type == "product_master":
                sku_val = str(record.get("sku") or "").strip()
                name_val = str(record.get("name") or "").strip()
                if not sku_val or sku_val == "nan":
                    row_errors.append("Missing SKU")
                if not name_val or name_val == "nan":
                    row_errors.append("Missing Product Name")
                record["mrp"] = float(record.get("mrp") or 0.0)
                record["cost_price"] = float(record.get("cost_price") or 0.0)

            # Record errors if any
            if row_errors:
                for err in row_errors:
                    errors.append({
                        "row_number": current_row_num,
                        "field": "row_validation",
                        "value": str(row.to_dict())[:80],
                        "reason": err,
                        "severity": "error"
                    })
            else:
                valid_records.append(record)

        invalid_count = len(errors)
        status = "completed" if len(valid_records) > 0 else "failed"

        return {
            "job_id": job_id,
            "data_type": data_type,
            "file_name": filename,
            "total_rows": total_rows,
            "valid_rows": len(valid_records),
            "invalid_rows": invalid_count,
            "duplicate_rows": duplicate_count,
            "warning_count": len(warnings),
            "status": status,
            "errors": errors[:50],  # first 50 errors for display
            "warnings": warnings[:50],
            "valid_records": valid_records
        }

    @staticmethod
    async def commit_import(job_id: str, data_type: str, filename: str, valid_records: List[Dict[str, Any]], stats: Dict[str, Any]):
        """Persists valid imported records into collection and logs job history."""
        target_coll_map = {
            "sales": "sales_transactions",
            "inventory": "inventory_snapshots",
            "purchases": "purchase_transactions",
            "product_master": "products",
            "store_master": "stores"
        }
        coll_name = target_coll_map.get(data_type, "sales_transactions")
        target_coll = db_manager.get_collection(coll_name)
        jobs_coll = db_manager.get_collection("import_jobs")

        if valid_records:
            await target_coll.insert_many(valid_records)

        # Log import job
        job_doc = {
            "job_id": job_id,
            "data_type": data_type,
            "file_name": filename,
            "file_size_bytes": stats.get("file_size_bytes", 0),
            "total_rows": stats.get("total_rows", len(valid_records)),
            "valid_rows": len(valid_records),
            "invalid_rows": stats.get("invalid_rows", 0),
            "duplicate_rows": stats.get("duplicate_rows", 0),
            "warning_count": stats.get("warning_count", 0),
            "status": "completed" if valid_records else "failed",
            "created_at": datetime.utcnow().isoformat(),
            "error_summary": f"Imported {len(valid_records)} valid rows with {stats.get('invalid_rows', 0)} invalid rows."
        }
        await jobs_coll.insert_one(job_doc)
        return job_doc

    @staticmethod
    async def get_import_history() -> List[Dict[str, Any]]:
        jobs_coll = db_manager.get_collection("import_jobs")
        jobs = await jobs_coll.find({})
        return sorted(jobs, key=lambda j: j.get("created_at", ""), reverse=True)
