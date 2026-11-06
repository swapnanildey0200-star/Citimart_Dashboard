# FEAT-001: 4-Step Retail Spreadsheet Ingestion Pipeline

**Feature ID:** FEAT-001  
**Module:** Upload & Ingestion Engine  
**Version:** 1.1.0  
**Status:** Implemented & Verified  
**Owner:** Data Engineering Team  

---

## 1. Problem & Business Value
Retail chain operations at Citimart receive POS and stock registers in various formatting styles across different branch systems. These files often feature metadata banners in the top rows, inconsistent column headers (e.g., "Bill Date" vs "Transaction Date"), and occasional corrupted records. A robust 4-step wizard empowers non-technical store clerks to upload files reliably without breaking the central analytics database.

## 2. Ingestion Stages
1. **File Selection & Preview:** User uploads `.xlsx`, `.xls`, or `.csv` (up to 25MB). Backend reads the file in memory, automatically detects the actual column header row, and generates a preview with 5 sample rows.
2. **Column Auto-Mapping & Manual Adjustment:** Backend fuzzy-maps retailer headers to Citimart schema fields (e.g. "Item Code" -> "sku"). Users can review and adjust mappings in an interactive UI.
3. **Strict Row-by-Row Validation:** Checks data types, positive quantity bounds, date normalization, and database duplicate checks.
4. **Batch Commit & Audit Logging:** Clean rows are committed in a batch to MongoDB Atlas; a full execution record with cleanliness score is saved to `import_jobs`.

## 3. Supported Retail Streams
- `sales`: POS sales transaction logs.
- `inventory`: Store-level stock count and valuation snapshots.
- `purchases`: Vendor purchase orders and Goods Receipt Notes (GRN).
- `products`: Master product catalog additions.
- `stores`: Store branch master definitions.

## 4. Verification Evidence
- Tested in `backend/tests/test_analytics_and_validation.py` (`test_auto_mapping_aliases`).
- Ingestion audit trail logged in `import_jobs` collection.

