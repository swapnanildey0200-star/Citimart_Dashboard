import urllib.request
import json

endpoints = [
    ("GET", "http://127.0.0.1:8000/api/health", None),
    ("POST", "http://127.0.0.1:8000/api/analytics/kpi-summary", {}),
    ("POST", "http://127.0.0.1:8000/api/analytics/sales-trend", {}),
    ("POST", "http://127.0.0.1:8000/api/analytics/department-performance", {}),
    ("POST", "http://127.0.0.1:8000/api/analytics/store-performance", {}),
    ("POST", "http://127.0.0.1:8000/api/inventory/summary", {}),
    ("POST", "http://127.0.0.1:8000/api/purchases/summary", {}),
    ("GET", "http://127.0.0.1:8000/api/alerts/decision-card", None),
    ("GET", "http://127.0.0.1:8000/api/alerts", None),
    ("GET", "http://127.0.0.1:8000/api/upload/history", None),
    ("GET", "http://127.0.0.1:8000/api/settings/metric-glossary", None)
]

print("Verifying Citimart Analytics API Endpoints:")
all_passed = True
for method, url, body in endpoints:
    data = json.dumps(body).encode("utf-8") if body is not None else None
    headers = {"Content-Type": "application/json"} if body is not None else {}
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            content = json.loads(resp.read().decode("utf-8"))
            path = url.split("8000")[1]
            print(f"  [PASS] {method:4} {path:35} -> 200 OK")
    except Exception as e:
        print(f"  [FAIL] {method:4} {url}: {e}")
        all_passed = False

if all_passed:
    print("\nALL 11 ENDPOINTS TESTED AND VERIFIED SUCCESSFULLY!")
