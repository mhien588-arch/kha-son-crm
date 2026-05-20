"""
Chuyển User Guide từ M56:P90 → I56:L90
Chạy một lần: python move_user_guide.py
"""
import os
from google.oauth2.service_account import Credentials
import gspread
from sheets_connector import SHEET_ID, WORKSHEET_NAME, CREDS_FILE

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


def main():
    creds = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
    client = gspread.authorize(creds)
    ws = client.open_by_key(SHEET_ID).worksheet(WORKSHEET_NAME)

    print("Đang đọc nội dung M56:R90...")
    values = ws.get("M56:R90")

    if not values or all(not any(cell for cell in row) for row in values):
        print("M56:R90 trống — không có gì để chuyển.")
        return

    # Chuẩn hóa về 4 cột (I,J,K,L) — lấy tối đa 4 cột đầu mỗi dòng
    padded = []
    for row in values:
        r = row[:4]
        r += [""] * (4 - len(r))
        padded.append(r)
    # Đảm bảo đủ 35 dòng (hàng 56–90)
    while len(padded) < 35:
        padded.append(["", "", "", ""])

    print("Xóa vùng M56:R90...")
    ws.batch_clear(["M56:R90"])

    print("Ghi nội dung vào I56:L90...")
    ws.update(values=padded, range_name="I56:L90", value_input_option="RAW")

    print("Áp định dạng tiêu đề I56:L56 (navy)...")
    ws.format("I56:L56", {
        "textFormat": {
            "bold": True,
            "fontSize": 11,
            "foregroundColor": {"red": 1, "green": 1, "blue": 1},
        },
        "backgroundColor": {"red": 0.051, "green": 0.278, "blue": 0.631},
    })
    ws.format("I57:L90", {
        "textFormat": {"bold": False},
    })

    print("✅ Xong! User Guide đã về lại I56:L90.")


if __name__ == "__main__":
    main()
