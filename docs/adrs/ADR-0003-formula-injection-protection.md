# ADR-0003: Formula-Injection Neutralization for Spreadsheet Exports

**Status:** Accepted  
**Date:** 2026-10-28  
**Author:** Citimart Security Team  
**Supercedes:** None  

---

## 1. Context & Problem Statement

Citimart users export sales, inventory, and purchase tables to CSV files for use in Microsoft Excel. In retail environments, SKU descriptions, styles, or vendor names might originate from untrusted or unvalidated POS terminals. If a description begins with `=`, `+`, `-`, or `@` (e.g. `=cmd|'/C calc'!A0`), Excel interprets the text as an executable dynamic formula (CWE-1236: CSV Formula Injection).

## 2. Decision

We implemented a centralized cell sanitizer `sanitize_csv_cell()` in `backend/app/routers/export.py`:

```python
def sanitize_csv_cell(value: Any) -> Any:
    if isinstance(value, str) and value.startswith(("=", "+", "-", "@")):
        return f"'{value}"
    return value
```

Any cell starting with a formula operator is prepended with a single apostrophe (`'`). When opened in Excel, the leading apostrophe instructs Excel to render the content purely as text, disabling formula execution while preserving readability.

## 3. Consequences

### Positive
- Prevents remote code execution and formula injection vulnerabilities on client machines.
- Zero performance impact on CSV export generation.
- Validated via automated unit tests in `backend/tests/test_analytics_and_validation.py`.

