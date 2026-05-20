"""
Sắp xếp lại dữ liệu CRM vào đúng vị trí trong bảng định dạng.
- Giữ nguyên header row 1
- Đưa 52 khách thật vào rows 2-53 (trong/tiếp bảng)
- Xóa demo + dòng thừa bên dưới
- Không xóa định dạng ô
"""
import os, gspread
from google.oauth2.service_account import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]
CREDS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "google_creds.json")
SHEET_ID   = "1syWcPK_YopGk2XtIYegDgHwnR6YPOHOoZmiN4ze-yjA"
WS_NAME    = "KhaSonGreenHome_CRM"

DEMO_NAMES = {"Nguyễn Văn An", "Trần Thị Bình", "Lê Văn Cường", "Phạm Minh Dũng", "Hoàng Thị Em"}

def main():
    creds  = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
    client = gspread.authorize(creds)
    ws     = client.open_by_key(SHEET_ID).worksheet(WS_NAME)

    all_rows = ws.get_all_values()
    header   = all_rows[0]        # row 1 — giữ nguyên
    data_rows = all_rows[1:]      # rows 2..N

    # Lọc: bỏ dòng trống + bỏ demo
    real = []
    skipped_empty = 0
    skipped_demo  = 0
    for r in data_rows:
        if all(c.strip() == "" for c in r):
            skipped_empty += 1
            continue
        name = r[0].strip()
        if name in DEMO_NAMES:
            skipped_demo += 1
            continue
        real.append(r)

    print(f"Dòng trống bỏ qua : {skipped_empty}")
    print(f"Dòng demo bỏ qua  : {skipped_demo}")
    print(f"Khách thật giữ lại: {len(real)}")

    if not real:
        print("Không còn dữ liệu thật. Dừng.")
        return

    # Số cột
    ncols = len(header)
    last_data_row = 1 + len(real)   # sheet row cuối có dữ liệu mới
    old_last_row  = len(all_rows)   # sheet row cuối hiện tại

    # Bước 1: Ghi dữ liệu thật vào A2:H(1+len(real))
    end_col = chr(ord('A') + ncols - 1)   # 'H' nếu 8 cột
    write_range = f"A2:{end_col}{last_data_row}"
    ws.update(write_range, real, value_input_option="USER_ENTERED")
    print(f"Đã ghi {len(real)} dòng vào {write_range}")

    # Bước 2: Xóa các dòng thừa bên dưới (nếu có)
    if old_last_row > last_data_row:
        clear_range = f"A{last_data_row + 1}:{end_col}{old_last_row}"
        ws.batch_clear([clear_range])
        print(f"Đã xóa vùng thừa {clear_range}")
    else:
        print("Không có vùng thừa cần xóa.")

    print(f"\n✅ Hoàn thành — {len(real)} khách trong bảng, bắt đầu từ row 2.")

if __name__ == "__main__":
    main()
