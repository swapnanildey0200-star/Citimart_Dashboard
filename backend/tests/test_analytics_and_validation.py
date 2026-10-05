import pytest
from app.services.analytics_service import calculate_growth_pct
from app.services.upload_service import UploadService
from app.routers.export import sanitize_csv_cell

def test_calculate_growth_pct():
    # Normal growth
    assert calculate_growth_pct(110.0, 100.0) == 10.0
    # Decline
    assert calculate_growth_pct(79.0, 100.0) == -21.0
    # Safe division when LY is zero
    assert calculate_growth_pct(50.0, 0.0) is None
    # Both zero
    assert calculate_growth_pct(0.0, 0.0) == 0.0

def test_sanitize_csv_cell():
    # Neutralize dangerous formula prefixes
    assert sanitize_csv_cell("=cmd|' /C calc'!A0") == "'=cmd|' /C calc'!A0"
    assert sanitize_csv_cell("+12345") == "'+12345"
    assert sanitize_csv_cell("-50") == "'-50"
    assert sanitize_csv_cell("@SUM(A1:A10)") == "'@SUM(A1:A10)"
    # Safe regular strings and numbers
    assert sanitize_csv_cell("Citimart Chowringhee") == "Citimart Chowringhee"
    assert sanitize_csv_cell(1599.0) == "1599.0"

def test_auto_mapping_aliases():
    headers = ["Bill Date", "Store", "Item Code", "Sum of Bill Qty", "Sum of Net Amt"]
    mapping = UploadService.get_auto_mapping("sales", headers)
    
    assert mapping["date"] == "Bill Date"
    assert mapping["store_id"] == "Store"
    assert mapping["sku"] == "Item Code"
    assert mapping["quantity"] == "Sum of Bill Qty"
    assert mapping["net_sales"] == "Sum of Net Amt"
