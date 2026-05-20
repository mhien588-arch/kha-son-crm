"""
Định dạng bảng CRM chuyên nghiệp cho Google Sheets — Kha Sơn Green Home
- Header: xanh đậm bất động sản, chữ trắng đậm
- Data rows: xen kẽ trắng / xanh nhạt
- Trạng thái: màu riêng từng loại (toàn hàng)
- Border, freeze header, căn chỉnh cột, độ rộng tối ưu
"""
import os, gspread
from google.oauth2.service_account import Credentials

SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
CREDS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'google_creds.json')
SHEET_ID   = '1syWcPK_YopGk2XtIYegDgHwnR6YPOHOoZmiN4ze-yjA'
WS_NAME    = 'KhaSonGreenHome_CRM'

# ── Bảng màu ──────────────────────────────────────────────
HEADER_BG     = '#1B5E20'  # xanh rừng đậm – BĐS chuyên nghiệp
HEADER_TEXT   = '#FFFFFF'
ROW_ODD       = '#F1F8E9'  # xanh lá nhạt nhất
ROW_EVEN      = '#FFFFFF'  # trắng

# Màu trạng thái (nền hàng)
C_MOI         = '#E3F2FD'  # xanh dương nhạt
C_CHAM        = '#FFF8E1'  # vàng nhạt
C_HEN         = '#FFE0B2'  # cam nhạt
C_CHOT        = '#C8E6C9'  # xanh lá nhạt
C_TU_CHOI     = '#EEEEEE'  # xám nhạt

BORDER_COLOR  = '#388E3C'  # xanh lá vừa
# ──────────────────────────────────────────────────────────

def rgb(hex_color):
    h = hex_color.lstrip('#')
    return {'red': int(h[0:2],16)/255, 'green': int(h[2:4],16)/255, 'blue': int(h[4:6],16)/255}

def solid_border(color_hex):
    return {'style': 'SOLID', 'width': 1, 'color': rgb(color_hex)}

def main():
    creds  = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
    client = gspread.authorize(creds)
    sp     = client.open_by_key(SHEET_ID)
    ws     = sp.worksheet(WS_NAME)
    sid    = ws.id

    # Đếm dòng thực tế
    data_rows = len(ws.get_all_values()) - 1  # trừ header
    END_ROW   = 1 + data_rows  # 0-indexed end (exclusive)
    print(f'Sheet: {data_rows} dòng dữ liệu, sheet_id={sid}')

    requests = []

    # ── 1. Freeze header ──────────────────────────────────
    requests.append({'updateSheetProperties': {
        'properties': {'sheetId': sid, 'gridProperties': {'frozenRowCount': 1}},
        'fields': 'gridProperties.frozenRowCount'
    }})

    # ── 2. Header row format ──────────────────────────────
    requests.append({'repeatCell': {
        'range': {'sheetId': sid, 'startRowIndex': 0, 'endRowIndex': 1,
                  'startColumnIndex': 0, 'endColumnIndex': 8},
        'cell': {'userEnteredFormat': {
            'backgroundColor': rgb(HEADER_BG),
            'textFormat': {
                'foregroundColor': rgb(HEADER_TEXT),
                'bold': True, 'fontSize': 11, 'fontFamily': 'Arial'
            },
            'horizontalAlignment': 'CENTER',
            'verticalAlignment': 'MIDDLE',
            'wrapStrategy': 'WRAP'
        }},
        'fields': 'userEnteredFormat(backgroundColor,textFormat,horizontalAlignment,verticalAlignment,wrapStrategy)'
    }})

    # ── 3. Header row height ──────────────────────────────
    requests.append({'updateDimensionProperties': {
        'range': {'sheetId': sid, 'dimension': 'ROWS', 'startIndex': 0, 'endIndex': 1},
        'properties': {'pixelSize': 42},
        'fields': 'pixelSize'
    }})

    # ── 4. Data rows — xen kẽ màu nền (banding) ──────────
    # Xóa banding cũ nếu có, rồi thêm mới
    existing = ws.spreadsheet.fetch_sheet_metadata()
    for s in existing.get('sheets', []):
        if s['properties']['sheetId'] == sid:
            for band in s.get('bandedRanges', []):
                requests.append({'deleteBanding': {'bandedRangeId': band['bandedRangeId']}})

    requests.append({'addBanding': {
        'bandedRange': {
            'range': {'sheetId': sid, 'startRowIndex': 1, 'endRowIndex': END_ROW + 1,
                      'startColumnIndex': 0, 'endColumnIndex': 8},
            'rowProperties': {
                'headerColor':     rgb(HEADER_BG),
                'firstBandColor':  rgb(ROW_ODD),
                'secondBandColor': rgb(ROW_EVEN),
            }
        }
    }})

    # ── 5. Data rows — font & alignment base ─────────────
    requests.append({'repeatCell': {
        'range': {'sheetId': sid, 'startRowIndex': 1, 'endRowIndex': END_ROW + 1,
                  'startColumnIndex': 0, 'endColumnIndex': 8},
        'cell': {'userEnteredFormat': {
            'textFormat': {'fontSize': 10, 'fontFamily': 'Arial'},
            'verticalAlignment': 'MIDDLE',
            'wrapStrategy': 'WRAP'
        }},
        'fields': 'userEnteredFormat(textFormat,verticalAlignment,wrapStrategy)'
    }})

    # ── 6. Căn giữa: B C D E G H | Căn trái: A F ─────────
    for col_range, align in [
        ({'startColumnIndex': 1, 'endColumnIndex': 5},  'CENTER'),   # B-E
        ({'startColumnIndex': 6, 'endColumnIndex': 8},  'CENTER'),   # G-H
        ({'startColumnIndex': 0, 'endColumnIndex': 1},  'LEFT'),     # A
        ({'startColumnIndex': 5, 'endColumnIndex': 6},  'LEFT'),     # F
    ]:
        r = {'sheetId': sid, 'startRowIndex': 1, 'endRowIndex': END_ROW + 1}
        r.update(col_range)
        requests.append({'repeatCell': {
            'range': r,
            'cell': {'userEnteredFormat': {'horizontalAlignment': align}},
            'fields': 'userEnteredFormat.horizontalAlignment'
        }})

    # ── 7. Độ rộng cột (pixels) ───────────────────────────
    col_widths = [155, 120, 120, 105, 120, 220, 110, 130]
    for i, w in enumerate(col_widths):
        requests.append({'updateDimensionProperties': {
            'range': {'sheetId': sid, 'dimension': 'COLUMNS',
                      'startIndex': i, 'endIndex': i + 1},
            'properties': {'pixelSize': w},
            'fields': 'pixelSize'
        }})

    # ── 8. Border toàn bảng ───────────────────────────────
    border = solid_border(BORDER_COLOR)
    requests.append({'updateBorders': {
        'range': {'sheetId': sid, 'startRowIndex': 0, 'endRowIndex': END_ROW + 1,
                  'startColumnIndex': 0, 'endColumnIndex': 8},
        'top':    border, 'bottom': border,
        'left':   border, 'right':  border,
        'innerHorizontal': solid_border('#A5D6A7'),
        'innerVertical':   solid_border('#A5D6A7'),
    }})

    # ── 9. Conditional formatting — màu theo Trạng thái ──
    # Cột E = index 4. Formula dùng $E để lock cột, check từng hàng
    status_rules = [
        ('Chốt cọc',        C_CHOT),
        ('Hẹn xem đất',     C_HEN),
        ('Đang chăm sóc',   C_CHAM),
        ('Từ chối',         C_TU_CHOI),
        ('Mới',             C_MOI),
    ]
    for status, color in status_rules:
        requests.append({'addConditionalFormatRule': {
            'rule': {
                'ranges': [{'sheetId': sid, 'startRowIndex': 1, 'endRowIndex': END_ROW + 1,
                            'startColumnIndex': 0, 'endColumnIndex': 8}],
                'booleanRule': {
                    'condition': {
                        'type': 'CUSTOM_FORMULA',
                        'values': [{'userEnteredValue': f'=$E2="{status}"'}]
                    },
                    'format': {'backgroundColor': rgb(color)}
                }
            },
            'index': 0
        }})

    # ── 10. Gộp & gửi tất cả requests ────────────────────
    print(f'Đang gửi {len(requests)} yêu cầu định dạng...')
    sp.batch_update({'requests': requests})
    print('Hoàn thành định dạng bảng!')

if __name__ == '__main__':
    main()
