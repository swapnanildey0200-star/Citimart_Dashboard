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
        "cogs": ["sum of cogs with gst", "cogs", "cost", "cost price", "std cost"],
        "bill_no": ["bill no", "bill no.", "bill number", "invoice no", "invoice number", "receipt no"],
        "is_void": ["isvoid", "is void", "void", "cancelled"]
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

TOTAL_ROW_MARKERS = ("total", "grand total", "sub total", "subtotal", "report total")
DATE_FORMATS = ("%d-%m-%Y", "%d/%m/%Y", "%d.%m.%Y", "%d-%b-%Y", "%d-%b-%y", "%d/%m/%y", "%Y-%m-%d", "%Y/%m/%d")


def _is_blank(val: Any) -> bool:
    if val is None:
        return True
    try:
        if pd.isna(val):
            return True
    except (TypeError, ValueError):
        pass
    return isinstance(val, str) and val.strip().lower() in ("", "nan", "none", "null", "-", "n/a")


def _clean_text(val: Any) -> str:
    """Trim, collapse internal whitespace, drop non-breaking spaces."""
    if _is_blank(val):
        return ""
    return re.sub(r"\s+", " ", str(val).replace("\xa0", " ")).strip()


def _clean_code(val: Any) -> str:
    """Item/bill codes: text form without Excel float artefacts (123.0 -> 123) or stray spaces."""
    if isinstance(val, float) and val.is_integer():
        val = int(val)
    return _clean_text(val).upper()


def _to_number(val: Any) -> Optional[float]:
    """Parses 1,234.50 / (250) / 12- / ₹ 99 / 5% style values. Returns None if blank, raises ValueError if junk."""
    if _is_blank(val):
        return None
    if isinstance(val, bool):
        return float(val)
    if isinstance(val, (int, float)):
        return float(val)
    s = _clean_text(val).replace(",", "").replace("₹", "").replace("Rs.", "").replace("Rs", "").strip()
    negative = False
    if s.startswith("(") and s.endswith(")"):
        negative, s = True, s[1:-1]
    if s.endswith("-"):
        negative, s = True, s[:-1]
    s = s.rstrip("%").strip()
    num = float(s)
    return -num if negative else num


def _to_date(val: Any) -> Optional[str]:
    """Returns YYYY-MM-DD or None. Handles datetimes, Excel serials and day-first text dates."""
    if _is_blank(val):
        return None
    if isinstance(val, (datetime, date, pd.Timestamp)):
        return val.strftime("%Y-%m-%d")
    if isinstance(val, (int, float)):
        if 20000 < val < 80000:
            return (datetime(1899, 12, 30) + pd.to_timedelta(val, unit="D")).strftime("%Y-%m-%d")
        return None
    s = _clean_text(val)
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(s, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    try:
        return pd.to_datetime(s, dayfirst=True).strftime("%Y-%m-%d")
    except Exception:
        return None


def _is_truthy(val: Any) -> bool:
    if isinstance(val, bool):
        return val
    if isinstance(val, (int, float)) and not _is_blank(val):
        return val != 0
    return _clean_text(val).lower() in ("true", "yes", "y", "1", "void", "voided")


class UploadService:
    @staticmethod
    def _read_dataframe(file_bytes: bytes, filename: str, header_row_idx: int) -> pd.DataFrame:
        """Reads the file with the header at the given 1-based row, then strips the junk around the table."""
        skip = max(0, header_row_idx - 1)
        if filename.lower().endswith((".xlsx", ".xls")):
            df = pd.read_excel(io.BytesIO(file_bytes), skiprows=skip, dtype=object)
        else:
            try:
                df = pd.read_csv(io.BytesIO(file_bytes), skiprows=skip, dtype=object, encoding="utf-8-sig")
            except UnicodeDecodeError:
                df = pd.read_csv(io.BytesIO(file_bytes), skiprows=skip, dtype=object, encoding="latin-1")

        df.columns = [_clean_text(c) for c in df.columns]
        # Drop unnamed / fully empty columns and fully empty rows (spacer rows, trailing blanks)
        df = df.loc[:, [c for c in df.columns if c and not c.lower().startswith("unnamed:")]]
        df = df.dropna(how="all")
        return df

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
        # Score = known-alias hits (weighted) + non-empty text cells; title rows like
        # "SALE DETAILS DAYWISE2" have few cells and no alias hits, so the real header wins.
        known_aliases = {a for fields in COLUMN_ALIASES.values() for al in fields.values() for a in al}
        best_header_idx = 0
        best_score = -1
        for idx, row in enumerate(raw_rows[:15]):
            cells = [c.strip().lower() for c in row if c and c.strip()]
            numeric = sum(1 for c in cells if re.fullmatch(r"[\d.,\-/: ]+", c))
            score = len(cells) + 3 * sum(1 for c in cells if c in known_aliases) - 2 * numeric
            if score > best_score:
                best_score = score
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

        def norm(s: str) -> str:
            return re.sub(r"[\s_]+", " ", s.lower().strip())

        usable = [(h, norm(h)) for h in headers if h and h.strip()]
        used: set = set()

        for target_field, aliases in target_fields.items():
            matched_header = None
            candidates = [norm(target_field)] + [norm(a) for a in aliases]
            # Pass 1: exact match, in alias priority order. Pass 2: alias contained in header.
            for exact in (True, False):
                for cand in candidates:
                    for h, clean_h in usable:
                        if h in used:
                            continue
                        if (clean_h == cand) if exact else (len(cand) >= 4 and cand in clean_h):
                            matched_header = h
                            break
                    if matched_header:
                        break
                if matched_header:
                    break
            if matched_header:
                used.add(matched_header)
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
        try:
            df = UploadService._read_dataframe(file_bytes, filename, header_row_idx)
        except Exception as e:
            return {
                "job_id": job_id, "data_type": data_type, "file_name": filename,
                "total_rows": 0, "valid_rows": 0, "invalid_rows": 0, "duplicate_rows": 0,
                "warning_count": 0, "status": "failed", "warnings": [], "valid_records": [],
                "errors": [{"row_number": 0, "field": "file", "value": None,
                            "reason": f"Unable to read file: {e}", "severity": "error"}],
            }

        valid_records = []
        errors = []
        warnings = []
        duplicate_count = 0
        seen_keys = set()
        invalid_row_nums = set()
        skipped = {"totals": 0, "void": 0}
        unknown_stores: Dict[str, List[int]] = {}
        unknown_skus: Dict[str, List[int]] = {}
        canonical_new_stores: Dict[str, str] = {}
        current_year = datetime.now().year

        # Remove report footer rows ("Total", "Grand Total") before they are counted as data
        def _is_total_row(r: pd.Series) -> bool:
            texts = [_clean_text(v).lower() for v in r.values if not _is_blank(v) and isinstance(v, str)]
            return bool(texts) and texts[0].rstrip(":") in TOTAL_ROW_MARKERS and len(texts) <= 2
        total_mask = df.apply(_is_total_row, axis=1) if len(df) else pd.Series([], dtype=bool)
        skipped["totals"] = int(total_mask.sum())
        df = df[~total_mask]
        total_rows = len(df)

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
            current_row_num = int(row_idx) + header_row_idx + 1
            row_errors = []
            record: Dict[str, Any] = {"import_job_id": job_id}

            # Map fields
            for target_field, mapped_col in mapping.items():
                if mapped_col and mapped_col in df.columns:
                    val = row[mapped_col]
                    record[target_field] = None if _is_blank(val) else val
                else:
                    record[target_field] = None

            # Validation logic by data type
            if data_type == "sales":
                # Voided bills are not sales: skip silently (counted in the cleaning summary)
                if _is_truthy(record.get("is_void")):
                    skipped["void"] += 1
                    continue

                # Date
                parsed_date = _to_date(record.get("date"))
                if record.get("date") is None:
                    row_errors.append("Missing transaction date")
                elif parsed_date is None:
                    row_errors.append(f"Invalid date format: {record.get('date')}")
                record["date"] = parsed_date

                # Store: match by id or name, case/space-insensitive
                store_val = _clean_text(record.get("store_id"))
                if not store_val:
                    row_errors.append("Missing store identifier")
                else:
                    ids_ci = {k.lower(): k for k in known_stores}
                    if store_val in known_stores:
                        record["store_id"] = store_val
                    elif store_val.lower() in ids_ci:
                        record["store_id"] = ids_ci[store_val.lower()]
                    elif store_val.lower() in store_name_to_id:
                        record["store_id"] = store_name_to_id[store_val.lower()]
                    else:
                        store_val = canonical_new_stores.setdefault(store_val.lower(), store_val)
                        unknown_stores.setdefault(store_val, []).append(current_row_num)
                        record["store_id"] = store_val

                # SKU
                sku_val = _clean_code(record.get("sku"))
                if not sku_val:
                    row_errors.append("Missing SKU / Item Code")
                else:
                    record["sku"] = sku_val
                    if known_products and sku_val not in known_products:
                        unknown_skus.setdefault(sku_val, []).append(current_row_num)

                # Numbers: parse leniently (commas, brackets, trailing minus)
                numeric = {}
                for fld in ("quantity", "net_sales", "selling_price", "gross_sales", "discount", "cogs"):
                    try:
                        numeric[fld] = _to_number(record.get(fld))
                    except ValueError:
                        numeric[fld] = None
                        if fld in ("quantity", "net_sales"):
                            row_errors.append(f"Invalid {fld.replace('_', ' ')}: {record.get(fld)}")
                if record.get("quantity") is None:
                    row_errors.append("Missing quantity")
                if record.get("net_sales") is None:
                    row_errors.append("Missing net sales amount")

                qty = numeric["quantity"] or 0.0
                net_sales = numeric["net_sales"] or 0.0
                record["quantity"] = qty
                record["net_sales"] = net_sales
                record["selling_price"] = numeric["selling_price"] or 0.0
                record["discount"] = numeric["discount"] or 0.0
                record["cogs"] = numeric["cogs"] or 0.0
                record["gross_sales"] = numeric["gross_sales"] if numeric["gross_sales"] is not None else net_sales + record["discount"]

                # Returns (negative qty and amount) are valid retail data; a sign mismatch is not
                if qty < 0 and net_sales > 0 or qty > 0 and net_sales < 0:
                    row_errors.append(f"Quantity ({qty:g}) and net amount ({net_sales:g}) have opposite signs")
                record["is_return"] = qty < 0

                # Period type (TY = current calendar year)
                record["period_type"] = "TY" if parsed_date and int(parsed_date[:4]) >= current_year else ("LY" if parsed_date else "TY")

                # Duplicates: same bill line when a bill number is mapped, else an identical full source row
                bill_no = _clean_code(record.get("bill_no"))
                if bill_no:
                    tx_key = f"{bill_no}|{record.get('date')}|{record.get('store_id')}|{record.get('sku')}|{qty}|{net_sales}"
                else:
                    tx_key = "|".join(_clean_text(v) for v in row.values)
                if tx_key in seen_keys:
                    # Identical lines on one bill are usually the same item scanned twice, so keep them and just report
                    duplicate_count += 1
                else:
                    seen_keys.add(tx_key)

                record.pop("bill_no", None)
                record.pop("is_void", None)
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
                invalid_row_nums.add(current_row_num)
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

        # One aggregated warning per unknown store / SKU instead of one per row
        for store_val, rows in unknown_stores.items():
            warnings.append({
                "row_number": rows[0], "field": "store_id", "value": store_val, "severity": "warning",
                "reason": f"Store '{store_val}' not found in Store Master ({len(rows)} rows). Will auto-register."
            })
        if unknown_skus:
            sample = ", ".join(list(unknown_skus)[:5])
            warnings.append({
                "row_number": min(r[0] for r in unknown_skus.values()), "field": "sku", "value": sample, "severity": "warning",
                "reason": f"{len(unknown_skus)} SKUs not found in Product Master (e.g. {sample})."
            })

        if duplicate_count:
            warnings.append({
                "row_number": 0, "field": "row_validation", "value": None, "severity": "warning",
                "reason": f"{duplicate_count} rows are identical to an earlier row (likely the same item scanned twice). They were kept."
            })

        status = "completed" if len(valid_records) > 0 else "failed"

        return {
            "job_id": job_id,
            "data_type": data_type,
            "file_name": filename,
            "total_rows": total_rows,
            "valid_rows": len(valid_records),
            "invalid_rows": len(invalid_row_nums),
            "duplicate_rows": duplicate_count,
            "warning_count": len(warnings),
            "status": status,
            "cleaning_summary": {
                "total_rows_removed": skipped["totals"],
                "void_rows_removed": skipped["void"],
                "unknown_stores": len(unknown_stores),
                "unknown_skus": len(unknown_skus),
            },
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
        await jobs_coll.insert_one(dict(job_doc))  # copy: the driver adds a non-serialisable _id
        return job_doc

    @staticmethod
    async def get_import_history() -> List[Dict[str, Any]]:
        jobs_coll = db_manager.get_collection("import_jobs")
        jobs = await jobs_coll.find({})
        return sorted(jobs, key=lambda j: j.get("created_at", ""), reverse=True)
