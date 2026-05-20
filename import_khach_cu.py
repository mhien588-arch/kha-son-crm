"""
Nhập dữ liệu khách hàng cũ từ sheet nguồn → sheet chính CRM
Nguồn: 12zUF0GNXB96eHyoW6XcxWmVqyOdwrYREWI5EPsuYIXw (gid=1976740888)
Đích:  1syWcPK_YopGk2XtIYegDgHwnR6YPOHOoZmiN4ze-yjA (KhaSonGreenHome_CRM)
"""
import os
import sys
import gspread
import pandas as pd
from datetime import date
from google.oauth2.service_account import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]
CREDS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "google_creds.json")

SOURCE_SHEET_ID = "12zUF0GNXB96eHyoW6XcxWmVqyOdwrYREWI5EPsuYIXw"
SOURCE_GID = 1976740888

TARGET_SHEET_ID = "1syWcPK_YopGk2XtIYegDgHwnR6YPOHOoZmiN4ze-yjA"
TARGET_WS_NAME = "KhaSonGreenHome_CRM"

TARGET_COLUMNS = [
    "Tên khách", "Số ĐT", "Nguồn", "Sale chăm sóc",
    "Trạng thái", "Ghi chú", "Ngày tiếp cận", "Ngày tương tác cuối",
]

# Mapping: cột nguồn (lowercase strip) → cột đích
COLUMN_MAP = {
    "tên khách hàng": "Tên khách",
    "tên khách":      "Tên khách",
    "họ tên":         "Tên khách",
    "họ và tên":      "Tên khách",
    "tên":            "Tên khách",
    "khách hàng":     "Tên khách",

    "số điện thoại":  "Số ĐT",
    "số đt":          "Số ĐT",
    "điện thoại":     "Số ĐT",
    "sđt":            "Số ĐT",
    "phone":          "Số ĐT",
    "số phone":       "Số ĐT",

    "nguồn":          "Nguồn",
    "kênh":           "Nguồn",
    "nguồn lead":     "Nguồn",
    "kênh tiếp thị":  "Nguồn",

    "sale":           "Sale chăm sóc",
    "sale chăm sóc":  "Sale chăm sóc",
    "người phụ trách": "Sale chăm sóc",
    "nhân viên":      "Sale chăm sóc",
    "nvkd":           "Sale chăm sóc",

    "trạng thái":     "Trạng thái",
    "tình trạng":     "Trạng thái",
    "status":         "Trạng thái",

    "ghi chú":        "Ghi chú",
    "note":           "Ghi chú",
    "notes":          "Ghi chú",
    "nội dung":       "Ghi chú",

    "ngày tiếp cận":  "Ngày tiếp cận",
    "ngày tạo":       "Ngày tiếp cận",
    "ngày":           "Ngày tiếp cận",
    "date":           "Ngày tiếp cận",
    "ngày nhập":      "Ngày tiếp cận",

    "ngày tương tác cuối": "Ngày tương tác cuối",
    "tương tác cuối":      "Ngày tương tác cuối",
    "lần cuối":            "Ngày tương tác cuối",
    "ngày cập nhật":       "Ngày tương tác cuối",
}

VALID_STATUS = {"Mới", "Đang chăm sóc", "Hẹn xem đất", "Chốt cọc", "Từ chối"}
DEFAULT_STATUS = "Mới"
TODAY = date.today().strftime("%Y-%m-%d")


def get_client():
    creds = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
    return gspread.authorize(creds)


def load_source(client):
    sh = client.open_by_key(SOURCE_SHEET_ID)
    # Tìm worksheet theo gid
    ws = None
    for w in sh.worksheets():
        if w.id == SOURCE_GID:
            ws = w
            break
    if ws is None:
        print(f"Không tìm thấy tab có gid={SOURCE_GID}. Danh sách tabs:")
        for w in sh.worksheets():
            print(f"  - {w.title!r} (gid={w.id})")
        sys.exit(1)
    print(f"Sheet nguồn: '{ws.title}' — đang tải dữ liệu...")
    records = ws.get_all_values()
    if not records:
        print("Sheet nguồn trống!")
        sys.exit(1)
    return records


def map_columns(records):
    headers_raw = records[0]
    headers_lower = [h.strip().lower() for h in headers_raw]

    print(f"\nCột sheet nguồn ({len(headers_raw)} cột):")
    for i, h in enumerate(headers_raw):
        mapped = COLUMN_MAP.get(h.strip().lower(), "— (bỏ qua)")
        print(f"  [{i}] {h!r}  →  {mapped}")

    # Xây dựng ánh xạ index nguồn → tên cột đích
    col_mapping = {}  # target_col_name -> source_col_index
    for i, h_lower in enumerate(headers_lower):
        if h_lower in COLUMN_MAP:
            target = COLUMN_MAP[h_lower]
            if target not in col_mapping:  # lấy cột đầu tiên khớp
                col_mapping[target] = i

    print(f"\nCột được ghép ({len(col_mapping)}/{len(TARGET_COLUMNS)} cột đích):")
    for tc in TARGET_COLUMNS:
        if tc in col_mapping:
            src_idx = col_mapping[tc]
            print(f"  ✅ {tc!r} ← cột [{src_idx}] {headers_raw[src_idx]!r}")
        else:
            print(f"  ⚠️  {tc!r} ← không tìm thấy → để trống")

    return col_mapping, headers_raw


def build_rows(records, col_mapping):
    data_rows = records[1:]  # bỏ header
    rows_out = []
    skipped = 0

    for r in data_rows:
        # Bỏ dòng hoàn toàn trống
        if all(c.strip() == "" for c in r):
            skipped += 1
            continue

        def get(target_col):
            if target_col not in col_mapping:
                return ""
            idx = col_mapping[target_col]
            val = r[idx].strip() if idx < len(r) else ""
            return val

        ten = get("Tên khách")
        sdt = get("Số ĐT")

        # Bỏ dòng không có tên lẫn SĐT
        if not ten and not sdt:
            skipped += 1
            continue

        trang_thai = get("Trạng thái")
        if trang_thai not in VALID_STATUS:
            trang_thai = DEFAULT_STATUS

        ngay_tiep_can = get("Ngày tiếp cận") or TODAY
        ngay_tuong_tac = get("Ngày tương tác cuối") or TODAY

        row = [
            ten,
            sdt,
            get("Nguồn") or "Khách cũ",
            get("Sale chăm sóc"),
            trang_thai,
            get("Ghi chú"),
            ngay_tiep_can,
            ngay_tuong_tac,
        ]
        rows_out.append(row)

    return rows_out, skipped


def append_to_target(client, rows):
    ws = client.open_by_key(TARGET_SHEET_ID).worksheet(TARGET_WS_NAME)
    print(f"\nĐang ghi {len(rows)} dòng vào sheet chính...")
    # Ghi từng batch 50 dòng để tránh timeout
    batch_size = 50
    for i in range(0, len(rows), batch_size):
        batch = rows[i:i + batch_size]
        ws.append_rows(batch, value_input_option="USER_ENTERED")
        print(f"  Đã ghi {min(i + batch_size, len(rows))}/{len(rows)} dòng...")
    return ws


def main():
    print("=" * 55)
    print("  NHẬP LIỆU KHÁCH HÀNG CŨ → CRM KHA SƠN GREEN HOME")
    print("=" * 55)

    client = get_client()
    print("Kết nối Google API thành công.")

    records = load_source(client)
    total_src = len(records) - 1
    print(f"Tải xong {total_src} dòng dữ liệu nguồn.")

    col_mapping, headers_raw = map_columns(records)
    rows, skipped = build_rows(records, col_mapping)

    print(f"\nTổng kết trước khi ghi:")
    print(f"  Dòng nguồn:      {total_src}")
    print(f"  Dòng hợp lệ:     {len(rows)}")
    print(f"  Dòng bỏ qua:     {skipped}")

    if not rows:
        print("\nKhông có dòng nào để nhập. Kết thúc.")
        return

    append_to_target(client, rows)

    print(f"\n{'=' * 55}")
    print(f"  HOÀN THÀNH — Đã nhập {len(rows)} khách hàng vào CRM")
    print(f"{'=' * 55}")


if __name__ == "__main__":
    main()
