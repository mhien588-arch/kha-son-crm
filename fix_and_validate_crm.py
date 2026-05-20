"""
Sửa dữ liệu + cài Dropdown Validation — Kha Sơn Green Home
Chạy 1 lần để:
  1. Chuẩn hoá Trạng thái, Sale, Nhu cầu, SĐT đang sai
  2. Cài dropdown (data validation) cho cột D/E/I để anh em nhập tay không bị sai
"""
import sys
import os
sys.stdout.reconfigure(encoding='utf-8')

import gspread
from google.oauth2.service_account import Credentials
from sheets_connector import load_config, SHEET_ID, WORKSHEET_NAME, CREDS_FILE, SCOPES

# ── Mapping sửa dữ liệu ───────────────────────────────────────────────────────

TRANG_THAI_VALID = ["Mới", "Đang chăm sóc", "Hẹn xem đất", "Từ chối", "Chốt cọc"]

NHU_CAU_VALID = ["Còn nhu cầu", "Không còn nhu cầu"]

TRANG_THAI_MAP = {
    # Chữ thường → viết hoa đúng
    "đang chăm sóc": "Đang chăm sóc",
    "từ chối":       "Từ chối",
    # Trim sẽ xử lý dấu cách thừa — map thêm phòng trường hợp còn sót
    "từ chối ":      "Từ chối",
    # Bị chặn = Từ chối
    "đã bị chặn":    "Từ chối",
    "Đã bị chặn":    "Từ chối",
    # Không liên lạc được → vẫn đang theo dõi
    "không liên lạc được":  "Đang chăm sóc",
    "không liên lạc được ": "Đang chăm sóc",
    "Không liên lạc được":  "Đang chăm sóc",
    "không liên lạc dc":    "Đang chăm sóc",
    # Đã hẹn / đã đến dự án → Hẹn xem đất
    "Tham khảo, hẹn gặp ":               "Hẹn xem đất",
    "Tham khảo, hẹn gặp":                "Hẹn xem đất",
    "Đã đến dự án, đang cân nhắc":        "Hẹn xem đất",
    # Mua chỗ khác / bỏ → Từ chối
    "Đã mua chỗ khác ": "Từ chối",
    "Đã mua chỗ khác":  "Từ chối",
    # Tìm hiểu → đang theo dõi
    "Tìm hiểu": "Đang chăm sóc",
    # Nhập nhầm
    "sale": "Đang chăm sóc",
}

SALE_MAP = {
    "Dung":   "Chị Dung",  # thiếu prefix, không khớp config
    "Dung ":  "Chị Dung",
}

NHU_CAU_MAP = {
    "Hết nhu cầu":    "Không còn nhu cầu",
    "Hết nhu cầu ":   "Không còn nhu cầu",
    "Đã mua chỗ khác": "Không còn nhu cầu",
    "còn khả năg":    "Còn nhu cầu",   # lỗi chính tả
    "còn khả năg ":   "Còn nhu cầu",
}


def fix_sdt(sdt: str) -> str:
    """Xoá khoảng trắng; nếu còn 9 chữ số không có số 0 đầu thì thêm 0."""
    s = sdt.replace(" ", "").replace("-", "").strip()
    if len(s) == 9 and not s.startswith("0") and s.isdigit():
        s = "0" + s
    return s


def rgb(h):
    h = h.lstrip('#')
    return {'red': int(h[0:2], 16)/255, 'green': int(h[2:4], 16)/255, 'blue': int(h[4:6], 16)/255}


def main():
    print("=" * 60)
    print("SỬA DỮ LIỆU + CÀI DROPDOWN VALIDATION")
    print("Kha Sơn Green Home — KhaSonGreenHome_CRM")
    print("=" * 60)

    cfg = load_config()
    sale_team = cfg.get("sale_team", ["Hiển", "Đức", "Sơn", "Tuấn Anh"])

    creds = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
    client = gspread.authorize(creds)
    ss = client.open_by_key(SHEET_ID)
    ws = ss.worksheet(WORKSHEET_NAME)
    sheet_id = ws.id

    # ── Đọc dữ liệu thô A:I ─────────────────────────────────────────────────
    print("\n[1] Đọc dữ liệu từ Sheet...")
    all_rows = ws.get("A:I")
    if not all_rows or len(all_rows) < 2:
        print("  Sheet trống, không có gì để sửa.")
        return

    header = all_rows[0]
    data_rows = all_rows[1:]
    total = len(data_rows)
    print(f"  Tìm thấy {total} dòng dữ liệu (row 2–{total+1})")

    # Col indices (0-based trong Python, nhưng ghi A:I nên A=0..I=8)
    COL_SDT    = 1   # B
    COL_SALE   = 3   # D
    COL_TT     = 4   # E
    COL_NC     = 8   # I

    # ── Bước 2: Chuẩn hoá Trạng thái ────────────────────────────────────────
    print("\n[2] Chuẩn hoá Trạng thái (cột E)...")
    tt_updates = []
    tt_count = 0
    for i, row in enumerate(data_rows):
        padded = row + [""] * (9 - len(row))
        original = padded[COL_TT]
        # Áp map (dựa trên giá trị gốc), sau đó fallback trim
        fixed = TRANG_THAI_MAP.get(original)
        if fixed is None:
            trimmed = original.strip()
            fixed = TRANG_THAI_MAP.get(trimmed, trimmed)
        # Nếu trimmed vẫn không có trong valid nhưng đã đúng chuẩn thì giữ nguyên
        if fixed not in TRANG_THAI_VALID and fixed == original.strip():
            fixed = original  # không thay đổi
        if fixed != original:
            sheet_row = i + 2
            tt_updates.append({"range": f"E{sheet_row}", "values": [[fixed]]})
            print(f"  Row {sheet_row}: [{original}] → [{fixed}]")
            tt_count += 1

    if tt_updates:
        ws.batch_update(tt_updates, value_input_option="RAW")
        print(f"  Đã sửa {tt_count} dòng Trạng thái.")
    else:
        print("  Không có Trạng thái nào cần sửa.")

    # ── Bước 3: Chuẩn hoá Sale chăm sóc ─────────────────────────────────────
    print("\n[3] Chuẩn hoá Sale chăm sóc (cột D)...")
    sale_updates = []
    sale_count = 0
    for i, row in enumerate(data_rows):
        padded = row + [""] * (9 - len(row))
        original = padded[COL_SALE]
        fixed = SALE_MAP.get(original, original.strip())
        if fixed != original:
            sheet_row = i + 2
            sale_updates.append({"range": f"D{sheet_row}", "values": [[fixed]]})
            print(f"  Row {sheet_row}: [{original}] → [{fixed}]")
            sale_count += 1

    if sale_updates:
        ws.batch_update(sale_updates, value_input_option="RAW")
        print(f"  Đã sửa {sale_count} dòng Sale.")
    else:
        print("  Không có Sale nào cần sửa.")

    # ── Bước 4: Chuẩn hoá Nhu cầu ────────────────────────────────────────────
    print("\n[4] Chuẩn hoá Nhu cầu (cột I)...")
    nc_updates = []
    nc_count = 0
    for i, row in enumerate(data_rows):
        padded = row + [""] * (9 - len(row))
        original = padded[COL_NC]
        fixed = NHU_CAU_MAP.get(original)
        if fixed is None:
            trimmed = original.strip()
            fixed = NHU_CAU_MAP.get(trimmed, trimmed)
        if fixed != original:
            sheet_row = i + 2
            nc_updates.append({"range": f"I{sheet_row}", "values": [[fixed]]})
            print(f"  Row {sheet_row}: [{original}] → [{fixed}]")
            nc_count += 1

    if nc_updates:
        ws.batch_update(nc_updates, value_input_option="RAW")
        print(f"  Đã sửa {nc_count} dòng Nhu cầu.")
    else:
        print("  Không có Nhu cầu nào cần sửa.")

    # ── Bước 5: Fix SĐT ───────────────────────────────────────────────────────
    print("\n[5] Fix SĐT (cột B) — xoá space, thêm số 0 đầu nếu thiếu...")
    sdt_updates = []
    sdt_count = 0
    for i, row in enumerate(data_rows):
        padded = row + [""] * (9 - len(row))
        original = padded[COL_SDT]
        fixed = fix_sdt(original)
        if fixed != original:
            sheet_row = i + 2
            sdt_updates.append({"range": f"B{sheet_row}", "values": [[fixed]]})
            print(f"  Row {sheet_row}: [{original}] → [{fixed}]")
            sdt_count += 1

    if sdt_updates:
        ws.batch_update(sdt_updates, value_input_option="RAW")
        print(f"  Đã sửa {sdt_count} SĐT.")
    else:
        print("  Không có SĐT nào cần sửa.")

    # ── Bước 6: Cài Dropdown Validation ──────────────────────────────────────
    print("\n[6] Cài Dropdown Validation cho cột D / E / I...")

    def one_of_list_rule(values, strict=True):
        return {
            "condition": {
                "type": "ONE_OF_LIST",
                "values": [{"userEnteredValue": v} for v in values],
            },
            "showCustomUi": True,
            "strict": strict,
        }

    def validation_request(col_index, rule, sheet_id_val):
        return {
            "setDataValidation": {
                "range": {
                    "sheetId": sheet_id_val,
                    "startRowIndex": 1,     # row 2 (0-indexed)
                    "endRowIndex": 300,     # đủ dự phòng 300 leads
                    "startColumnIndex": col_index,
                    "endColumnIndex": col_index + 1,
                },
                "rule": rule,
            }
        }

    requests = [
        # Cột D (index 3) — Sale chăm sóc
        validation_request(3, one_of_list_rule(sale_team), sheet_id),
        # Cột E (index 4) — Trạng thái
        validation_request(4, one_of_list_rule(TRANG_THAI_VALID), sheet_id),
        # Cột I (index 8) — Nhu cầu (không strict vì có thể để trống)
        validation_request(8, one_of_list_rule(NHU_CAU_VALID, strict=False), sheet_id),
    ]

    ss.batch_update({"requests": requests})
    print(f"  Cột D — Sale: {sale_team}")
    print(f"  Cột E — Trạng thái: {TRANG_THAI_VALID}")
    print(f"  Cột I — Nhu cầu: {NHU_CAU_VALID}")
    print("  Dropdown đã cài xong!")

    # ── Bước 7: Cài Date Picker cho cột G / H ────────────────────────────────
    print("\n[7] Cài Date Picker cho cột G (Ngày tiếp cận) và H (Ngày tương tác cuối)...")

    def date_validation_request(col_index, sheet_id_val):
        return {
            "setDataValidation": {
                "range": {
                    "sheetId": sheet_id_val,
                    "startRowIndex": 1,
                    "endRowIndex": 300,
                    "startColumnIndex": col_index,
                    "endColumnIndex": col_index + 1,
                },
                "rule": {
                    "condition": {"type": "DATE_IS_VALID"},
                    "showCustomUi": True,
                    "strict": False,
                },
            }
        }

    date_requests = [
        date_validation_request(6, sheet_id),   # Cột G — Ngày tiếp cận
        date_validation_request(7, sheet_id),   # Cột H — Ngày tương tác cuối
    ]
    ss.batch_update({"requests": date_requests})
    print("  Cột G — Ngày tiếp cận    : Date Picker ✓")
    print("  Cột H — Ngày tương tác cuối : Date Picker ✓")
    print("  Click ô G/H → chọn ngày từ lịch (hoặc gõ tay YYYY-MM-DD)")

    # ── Tổng kết ──────────────────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("TỔNG KẾT")
    print(f"  Trạng thái đã sửa : {tt_count} dòng")
    print(f"  Sale đã sửa       : {sale_count} dòng")
    print(f"  Nhu cầu đã sửa    : {nc_count} dòng")
    print(f"  SĐT đã sửa        : {sdt_count} dòng")
    print(f"  Dropdown đã cài   : 3 cột (D, E, I)")
    print(f"  Date Picker đã cài: 2 cột (G, H)")
    print()
    print("Mở Google Sheet → click ô G/H → thấy lịch chọn ngày là OK!")
    print("=" * 60)


if __name__ == "__main__":
    main()
