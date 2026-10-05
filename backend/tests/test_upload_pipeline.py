import urllib.request
import json
import io

def test_full_upload_pipeline():
    print("Testing Complete Upload & Validation Pipeline:")

    # 1. Download template
    url_tmpl = "http://127.0.0.1:8000/api/upload/template/sales"
    with urllib.request.urlopen(url_tmpl) as resp:
        sample_csv = resp.read()
        print(f"  [PASS] Downloaded sales template ({len(sample_csv)} bytes)")

    # 2. Upload Preview
    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="data_type"\r\n\r\n'
        f"sales\r\n"
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="test_sales_upload.csv"\r\n'
        f"Content-Type: text/csv\r\n\r\n"
        f"{sample_csv.decode('utf-8')}\r\n"
        f"--{boundary}--\r\n"
    ).encode("utf-8")

    req = urllib.request.Request(
        "http://127.0.0.1:8000/api/upload/preview",
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST"
    )

    with urllib.request.urlopen(req) as resp:
        preview = json.loads(resp.read().decode("utf-8"))
        print(f"  [PASS] Preview detected {len(preview['headers'])} headers: {preview['headers'][:4]}")
        mapping = preview["suggested_mapping"]
        assert mapping["sku"] is not None
        assert mapping["net_sales"] is not None

    # 3. Validate
    mapping_str = json.dumps(mapping)
    body_val = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="data_type"\r\n\r\n'
        f"sales\r\n"
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="mapping"\r\n\r\n'
        f"{mapping_str}\r\n"
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="header_row_idx"\r\n\r\n'
        f"1\r\n"
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="test_sales_upload.csv"\r\n'
        f"Content-Type: text/csv\r\n\r\n"
        f"{sample_csv.decode('utf-8')}\r\n"
        f"--{boundary}--\r\n"
    ).encode("utf-8")

    req_val = urllib.request.Request(
        "http://127.0.0.1:8000/api/upload/validate",
        data=body_val,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST"
    )

    with urllib.request.urlopen(req_val) as resp:
        val_res = json.loads(resp.read().decode("utf-8"))
        print(f"  [PASS] Validation passed: {val_res['valid_rows']} valid rows, {val_res['invalid_rows']} invalid rows, {val_res['duplicate_rows']} duplicates")
        assert val_res["valid_rows"] > 0

    # 4. Commit
    commit_payload = {
        "job_id": val_res["job_id"],
        "data_type": "sales",
        "file_name": "test_sales_upload.csv",
        "valid_records": val_res["valid_records"],
        "stats": {
            "total_rows": val_res["total_rows"],
            "invalid_rows": val_res["invalid_rows"],
            "duplicate_rows": val_res["duplicate_rows"],
            "warning_count": val_res["warning_count"]
        }
    }
    data_com = json.dumps(commit_payload).encode("utf-8")
    req_com = urllib.request.Request(
        "http://127.0.0.1:8000/api/upload/commit",
        data=data_com,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req_com) as resp:
        com_res = json.loads(resp.read().decode("utf-8"))
        print(f"  [PASS] Commit successful! Job ID: {com_res['import_job']['job_id']}")

    print("\nUPLOAD AND VALIDATION PIPELINE FULLY VERIFIED END-TO-END!")

if __name__ == "__main__":
    test_full_upload_pipeline()
