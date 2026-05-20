"""
Kết nối Google Sheets — Kha Sơn Green Home
Dùng chung cho tracker.py và daily_report.py
"""
import os
import json
import time
from datetime import date
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
from gspread.exceptions import APIError

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]
_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDS_FILE = os.path.join(_BASE_DIR, "data", "google_creds.json")
CONFIG_FILE = os.path.join(_BASE_DIR, "config.json")

_DEFAULTS = {
    "sheet_id": "1syWcPK_YopGk2XtIYegDgHwnR6YPOHOoZmiN4ze-yjA",
    "worksheet_name": "KhaSonGreenHome_CRM",
    "sale_team": ["Hiển", "Đức", "Sơn", "Tuấn Anh"],
    "remind_days": 3,
}


def load_config() -> dict:
    """Đọc config.json; nếu file chưa tồn tại trả về defaults."""
    try:
        with open(CONFIG_FILE, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return dict(_DEFAULTS)


def save_config(cfg: dict):
    """Ghi dict cfg vào config.json (UTF-8, indent 2)."""
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)


_cfg = load_config()
SHEET_ID = _cfg.get("sheet_id", _DEFAULTS["sheet_id"])
WORKSHEET_NAME = _cfg.get("worksheet_name", _DEFAULTS["worksheet_name"])

COLUMNS = [
    "Tên khách", "Số ĐT", "Nguồn", "Sale chăm sóc",
    "Trạng thái", "Ghi chú", "Ngày tiếp cận", "Ngày tương tác cuối",
    "Nhu cầu",  # cột I — Còn nhu cầu / Không còn nhu cầu / (trống)
]

STAGING_TAB = "SỐ MỚI KS"
STAGING_COLS = COLUMNS + ["✓ Đã xử lý"]


def _get_credentials() -> Credentials:
    """Thử Streamlit Secrets trước (khi chạy trên cloud), fallback về file local."""
    try:
        import streamlit as st
        if hasattr(st, "secrets") and "google_credentials" in st.secrets:
            return Credentials.from_service_account_info(
                dict(st.secrets["google_credentials"]), scopes=SCOPES
            )
    except Exception:
        pass
    return Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)


def retry_api_call(max_retries=5, initial_backoff=2):
    """Decorator tự động thử lại khi gặp lỗi API 429 Quota Exceeded."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            backoff = initial_backoff
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except APIError as e:
                    status_code = getattr(e, 'code', None)
                    if not status_code:
                        try:
                            status_code = e.response.status_code
                        except AttributeError:
                            pass
                    
                    is_429 = (status_code == 429) or ("429" in str(e)) or ("RESOURCE_EXHAUSTED" in str(e))
                    
                    if is_429 and attempt < max_retries - 1:
                        print(f"⚠️ [API 429] Vượt giới hạn Google Sheets API. Đang tự động ngủ {backoff}s và thử lại... (Lần {attempt + 1}/{max_retries})")
                        time.sleep(backoff)
                        backoff *= 2
                    else:
                        raise e
                except Exception as e:
                    raise e
        return wrapper
    return decorator


@retry_api_call()
def _get_ws():
    creds = _get_credentials()
    client = gspread.authorize(creds)
    return client.open_by_key(SHEET_ID).worksheet(WORKSHEET_NAME)


@retry_api_call()
def load_data() -> pd.DataFrame:
    ws = _get_ws()
    rows = ws.get("A:I")  # 9 cột: A-H data + I Nhu cầu
    if not rows or len(rows) < 2:
        return pd.DataFrame(columns=COLUMNS)
    data_rows = []
    sheet_row_indices = []
    for i, row in enumerate(rows[1:], start=2):
        if not row or not row[0].strip():  # bỏ dòng trống (User Guide cũ tại I56:L90 có A trống)
            continue
        data_rows.append(row + [""] * (9 - len(row)))
        sheet_row_indices.append(i)
    if not data_rows:
        return pd.DataFrame(columns=COLUMNS)
    # index = sheet row thực tế (không phải 0-based) để tránh tính sai khi có hàng trống
    return pd.DataFrame(data_rows, columns=COLUMNS, index=sheet_row_indices).fillna("")


@retry_api_call()
def append_row(row_dict: dict):
    ws = _get_ws()
    row = [str(row_dict.get(c, "")) for c in COLUMNS]
    # Tính next_row từ cột A — tránh bị User Guide (M56:P90) đánh lừa Sheets API
    next_row = len([v for v in ws.col_values(1) if v]) + 1
    ws.update(values=[row], range_name=f"A{next_row}:I{next_row}", value_input_option="RAW")


@retry_api_call()
def update_row(sheet_row_index: int, row_dict: dict):
    """sheet_row_index: 1-based index trong Sheet (hàng 2 = dữ liệu đầu tiên)."""
    ws = _get_ws()
    row = [str(row_dict.get(c, "")) for c in COLUMNS]
    ws.update(values=[row], range_name=f"A{sheet_row_index}:I{sheet_row_index}", value_input_option="RAW")


@retry_api_call()
def delete_crm_row(sheet_row_index: int):
    """Xóa 1 dòng khỏi CRM theo sheet row index (1-based)."""
    ws = _get_ws()
    ws.delete_rows(int(sheet_row_index))


@retry_api_call()
def highlight_new_row(sheet_row_index: int):
    """In đậm dòng lead mới — giúp sale nhận ra ngay trong Google Sheets."""
    ws = _get_ws()
    ws.format(f"A{sheet_row_index}:I{sheet_row_index}", {"textFormat": {"bold": True}})


@retry_api_call()
def unhighlight_row(sheet_row_index: int):
    """Bỏ đậm khi sale đã cập nhật trạng thái (không còn 'Mới')."""
    ws = _get_ws()
    ws.format(f"A{sheet_row_index}:I{sheet_row_index}", {"textFormat": {"bold": False}})


@retry_api_call()
def migrate_user_guide():
    """Chuyển User Guide từ I56:L90 → M56:P90 (chạy 1 lần khi thêm cột Nhu cầu).
    Đồng thời ghi header 'Nhu cầu' vào I1."""
    creds = _get_credentials()
    client = gspread.authorize(creds)
    ss = client.open_by_key(SHEET_ID)
    ws = ss.worksheet(WORKSHEET_NAME)
    i1_val = ws.acell("I1").value
    if i1_val and i1_val.strip() == "Nhu cầu":
        return  # Đã migrate rồi
    # Di chuyển User Guide: đọc giá trị I56:L90 → ghi M56:P90
    ug_values = ws.get("I56:L90")
    if ug_values:
        padded = [row + [""] * (4 - len(row)) for row in ug_values]
        ws.update(values=padded, range_name="M56:P90", value_input_option="RAW")
        # Định dạng tiêu đề User Guide ở M56
        ws.format("M56:P56", {"textFormat": {"bold": True, "fontSize": 11},
                               "backgroundColor": {"red": 0.051, "green": 0.278, "blue": 0.631}})
        ws.format("M57:P90", {"textFormat": {"bold": False}})
    # Xóa nội dung cũ I56:L90
    ws.batch_clear(["I56:L90"])
    # Ghi header "Nhu cầu" vào I1
    ws.update(values=[["Nhu cầu"]], range_name="I1", value_input_option="RAW")
    ws.format("I1", {"textFormat": {"bold": True, "foregroundColor": {"red": 1, "green": 1, "blue": 1}},
                     "backgroundColor": {"red": 0.051, "green": 0.278, "blue": 0.631}})


# ── STAGING TAB "SỐ MỚI KS" ───────────────────────────────────────────────

@retry_api_call()
def ensure_staging_tab():
    """Lấy hoặc tạo mới tab staging 'SỐ MỚI KS' với header + checkbox cột I."""
    creds = _get_credentials()
    client = gspread.authorize(creds)
    ss = client.open_by_key(SHEET_ID)
    try:
        ws = ss.worksheet(STAGING_TAB)
    except gspread.exceptions.WorksheetNotFound:
        ws = ss.add_worksheet(title=STAGING_TAB, rows=200, cols=9)
        ws.update(values=[STAGING_COLS], range_name="A1:I1")
        ws.format("A1:I1", {
            "textFormat": {"bold": True},
            "backgroundColor": {"red": 1.0, "green": 0.976, "blue": 0.769},
        })
        ws.freeze(rows=1)
        ss.batch_update({"requests": [{
            "setDataValidation": {
                "range": {
                    "sheetId": ws.id,
                    "startRowIndex": 1,
                    "endRowIndex": 200,
                    "startColumnIndex": 8,
                    "endColumnIndex": 9,
                },
                "rule": {"condition": {"type": "BOOLEAN"}, "strict": True},
            }
        }]})
    return ws


@retry_api_call()
def append_staging_row(row_dict: dict):
    """Thêm lead mới vào tab staging với checkbox FALSE (chưa xử lý)."""
    ws = ensure_staging_tab()
    data_row = [str(row_dict.get(c, "")) for c in COLUMNS[:8]]  # A:H, bỏ "Nhu cầu" (cột I staging là checkbox)
    # Dùng col_values(1) thay vì append_row vì BOOLEAN validation trên I2:I200
    # khiến append_row tưởng bảng đầy đến row 200 → ghi vào row 201 (ngoài tầm nhìn)
    col_a = ws.col_values(1)
    next_row = max(len(col_a) + 1, 2)
    # RAW để giữ số 0 đầu SĐT (USER_ENTERED xử lý "0978..." thành số → mất số 0)
    ws.update(values=[data_row], range_name=f"A{next_row}:H{next_row}", value_input_option="RAW")
    # Cột I để trống → checkbox tự hiện unchecked do BOOLEAN data validation


@retry_api_call()
def load_staging_data():
    """Đọc tab staging — trả về (DataFrame 8 cột, list sheet_row_indices)."""
    ws = ensure_staging_tab()
    rows = ws.get("A:I")
    if not rows or len(rows) < 2:
        return pd.DataFrame(columns=COLUMNS), []
    records, sheet_indices = [], []
    for i, row in enumerate(rows[1:], start=2):
        padded = row + [""] * (9 - len(row))
        if not padded[0].strip():  # bỏ qua dòng trống (checkbox data validation tạo 199 dòng giả)
            continue
        records.append(padded[:8])
        sheet_indices.append(i)
    df = pd.DataFrame(records, columns=COLUMNS[:8]).fillna("") if records else pd.DataFrame(columns=COLUMNS[:8])
    return df, sheet_indices


@retry_api_call()
def transfer_checked_leads() -> list:
    """Chuyển các dòng đã tích ✓ từ staging vào CRM. Trả về list tên khách đã chuyển."""
    ws = ensure_staging_tab()
    rows = ws.get("A:I")
    if not rows or len(rows) < 2:
        return []
    checked = []
    for i, row in enumerate(rows[1:], start=2):
        padded = row + [""] * (9 - len(row))
        if str(padded[8]).strip().upper() == "TRUE":
            checked.append((dict(zip(COLUMNS, padded[:8])), i))
    if not checked:
        return []
    cdf = load_data()
    base_row = (max(cdf.index) + 1) if not cdf.empty else 2
    for i, (row_dict, _) in enumerate(checked):
        append_row(row_dict)
        highlight_new_row(base_row + i)
    for _, sheet_row in sorted(checked, key=lambda x: x[1], reverse=True):
        ws.delete_rows(sheet_row)
    return [rd["Tên khách"] for rd, _ in checked]


def backup_to_csv() -> bool:
    """Tải toàn bộ dữ liệu CRM hiện tại và sao lưu thành file CSV cục bộ hằng ngày."""
    try:
        df = load_data()
        if df.empty:
            print("⚠️ [Sao Lưu] Dữ liệu CRM trống. Hủy sao lưu để tránh ghi đè dữ liệu cũ.")
            return False
        
        backup_dir = os.path.join(_BASE_DIR, "data", "backups")
        os.makedirs(backup_dir, exist_ok=True)
        
        today_str = date.today().strftime("%Y-%m-%d")
        backup_file = os.path.join(backup_dir, f"crm_backup_{today_str}.csv")
        
        # UTF-8 with BOM (utf-8-sig) giúp Excel mở trực tiếp hiển thị đúng tiếng Việt
        df.to_csv(backup_file, encoding="utf-8-sig", index=True)
        print(f"💾 [Sao Lưu] Đã sao lưu dữ liệu CRM thành công vào: {backup_file}")
        return True
    except Exception as e:
        print(f"❌ [Sao Lưu] Lỗi khi thực hiện sao lưu tự động: {e}")
        return False


if __name__ == "__main__":
    print("Đang kết nối Google Sheets...")
    df = load_data()
    if df.empty:
        print("Sheet trống hoặc chưa có dữ liệu.")
    else:
        print(f"Kết nối thành công! Tìm thấy {len(df)} khách hàng:\n")
        print(df[["Tên khách", "Số ĐT", "Trạng thái", "Sale chăm sóc"]].to_string(index=False))
