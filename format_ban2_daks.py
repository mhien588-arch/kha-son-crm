"""
Tạo và định dạng tab "Khach_Hang_Ban2 DA KS" — Kha Sơn Green Home
- Tạo tab mới với header 8 cột
- Header: xanh navy đậm, chữ trắng bold
- Banding xen kẽ xanh nhạt / trắng
- Conditional formatting theo Trạng thái
- Border chuyên nghiệp
- User Guide tại I56:L90
"""
import os
import gspread
from google.oauth2.service_account import Credentials

SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
CREDS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'google_creds.json')
SHEET_ID = '1syWcPK_YopGk2XtIYegDgHwnR6YPOHOoZmiN4ze-yjA'
TAB_NAME = 'Khach_Hang_Ban2 DA KS'

COLUMNS = ['Tên khách', 'Số ĐT', 'Nguồn', 'Sale chăm sóc',
           'Trạng thái', 'Ghi chú', 'Ngày tiếp cận', 'Ngày tương tác cuối']

# ── Bảng màu ──────────────────────────────────────────────────────────────────
HEADER_BG   = '#0D47A1'  # navy đậm — BĐS chuyên nghiệp
HEADER_TEXT = '#FFFFFF'
ROW_ODD     = '#E8F4FD'  # xanh nhạt
ROW_EVEN    = '#FFFFFF'

C_MOI       = '#E3F2FD'  # xanh dương nhạt
C_CHAM      = '#FFF9C4'  # vàng nhạt
C_HEN       = '#FFE0B2'  # cam nhạt
C_CHOT      = '#C8E6C9'  # xanh lá nhạt
C_TU_CHOI   = '#EEEEEE'  # xám nhạt

GUIDE_HEADER_BG   = '#0D47A1'
GUIDE_SECTION_BG  = '#E3F2FD'
GUIDE_SECTION_FG  = '#0D47A1'
GUIDE_META_BG     = '#BBDEFB'
BORDER_OUTER      = '#1565C0'
BORDER_INNER      = '#90CAF9'
GUIDE_BORDER      = '#90CAF9'
# ──────────────────────────────────────────────────────────────────────────────


def rgb(hex_color):
    h = hex_color.lstrip('#')
    return {'red': int(h[0:2], 16) / 255,
            'green': int(h[2:4], 16) / 255,
            'blue': int(h[4:6], 16) / 255}


def solid_border(color_hex, width=1):
    return {'style': 'SOLID', 'width': width, 'color': rgb(color_hex)}


def cell_format(bg=None, fg=None, bold=False, italic=False,
                font_size=10, h_align='LEFT', v_align='MIDDLE',
                wrap=True, font_family='Arial'):
    fmt = {
        'textFormat': {
            'bold': bold, 'italic': italic,
            'fontSize': font_size, 'fontFamily': font_family,
        },
        'horizontalAlignment': h_align,
        'verticalAlignment': v_align,
        'wrapStrategy': 'WRAP' if wrap else 'OVERFLOW_CELL',
    }
    if bg:
        fmt['backgroundColor'] = rgb(bg)
    if fg:
        fmt['textFormat']['foregroundColor'] = rgb(fg)
    return fmt


def repeat_cell(sid, r1, r2, c1, c2, fmt, fields=None):
    if fields is None:
        fields = 'userEnteredFormat'
    return {'repeatCell': {
        'range': {'sheetId': sid, 'startRowIndex': r1, 'endRowIndex': r2,
                  'startColumnIndex': c1, 'endColumnIndex': c2},
        'cell': {'userEnteredFormat': fmt},
        'fields': fields,
    }}


def merge_req(sid, r1, r2, c1, c2):
    return {'mergeCells': {
        'range': {'sheetId': sid, 'startRowIndex': r1, 'endRowIndex': r2,
                  'startColumnIndex': c1, 'endColumnIndex': c2},
        'mergeType': 'MERGE_ALL',
    }}


def dim_req(sid, dimension, start, end, size):
    return {'updateDimensionProperties': {
        'range': {'sheetId': sid, 'dimension': dimension,
                  'startIndex': start, 'endIndex': end},
        'properties': {'pixelSize': size},
        'fields': 'pixelSize',
    }}


def borders_req(sid, r1, r2, c1, c2, outer_color, inner_color):
    return {'updateBorders': {
        'range': {'sheetId': sid, 'startRowIndex': r1, 'endRowIndex': r2,
                  'startColumnIndex': c1, 'endColumnIndex': c2},
        'top':           solid_border(outer_color, 2),
        'bottom':        solid_border(outer_color, 2),
        'left':          solid_border(outer_color, 2),
        'right':         solid_border(outer_color, 2),
        'innerHorizontal': solid_border(inner_color),
        'innerVertical':   solid_border(inner_color),
    }}


def main():
    creds  = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
    client = gspread.authorize(creds)
    sp     = client.open_by_key(SHEET_ID)

    # ── 1. Tạo tab mới (hoặc dùng lại nếu đã có) ─────────────────────────────
    existing_titles = [ws.title for ws in sp.worksheets()]
    if TAB_NAME in existing_titles:
        ws = sp.worksheet(TAB_NAME)
        print(f'Tab "{TAB_NAME}" đã tồn tại, tiếp tục định dạng...')
    else:
        ws = sp.add_worksheet(title=TAB_NAME, rows=200, cols=20)
        print(f'Đã tạo tab mới: "{TAB_NAME}"')

    sid = ws.id

    # ── 2. Ghi header row ─────────────────────────────────────────────────────
    ws.update(values=[COLUMNS], range_name='A1:H1', value_input_option='USER_ENTERED')
    print('Đã ghi header row.')

    # ── 3. Ghi User Guide content (I56:I90) ───────────────────────────────────
    guide_data = [
        # row 56 — tiêu đề chính (merge I56:L56)
        ['═══  HƯỚNG DẪN SỬ DỤNG  —  KHA SƠN GREEN HOME  ═══', '', '', ''],
        # row 57 — phụ đề
        ['Dự án Đất nền KCN Phú Bình, Thái Nguyên  |  Triển khai từ: 17/05/2026  |  Hotline: 0368.557.832', '', '', ''],
        # row 58 — trống
        ['', '', '', ''],
        # row 59 — section header: MÀU SẮC
        ['MÀU SẮC TRẠNG THÁI', '', '', ''],
        # row 60–64 — từng trạng thái
        ['Mới           → Nền xanh dương nhạt  —  Chưa liên hệ', '', '', ''],
        ['Đang chăm sóc → Nền vàng nhạt         —  Đang theo dõi', '', '', ''],
        ['Hẹn xem đất   → Nền cam nhạt           —  Đã hẹn lịch đi xem đất', '', '', ''],
        ['Chốt cọc      → Nền xanh lá nhạt       —  Đã đặt cọc  (THẮNG)', '', '', ''],
        ['Từ chối       → Nền xám nhạt           —  Không mua  (thua)', '', '', ''],
        # row 65 — trống
        ['', '', '', ''],
        # row 66 — section header: QUY TRÌNH
        ['QUY TRÌNH CẬP NHẬT HÀNG NGÀY', '', '', ''],
        # row 67–69
        ['Sáng  (8:00)  —  Mở Mo Tracker.bat → [3] Kiểm tra khách quá 3 ngày → Gọi ngay', '', '', ''],
        ['Chiều (17:00) —  Mở Mo Tracker.bat → [5] Cập nhật trạng thái khách', '', '', ''],
        ['Tối   (18:00) —  Mở Bao Cao Ngay.bat → Xem KPI → Chụp màn hình gửi Zalo team', '', '', ''],
        # row 70 — trống
        ['', '', '', ''],
        # row 71 — section header: TRẠNG THÁI
        ['TRẠNG THÁI HỢP LỆ  (chỉ nhập đúng 1 trong 5 giá trị)', '', '', ''],
        # row 72
        ['Mới   |   Đang chăm sóc   |   Hẹn xem đất   |   Chốt cọc   |   Từ chối', '', '', ''],
        # row 73 — trống
        ['', '', '', ''],
        # row 74 — section header: PHÂN CÔNG
        ['PHÂN CÔNG SALE', '', '', ''],
        # row 75–78
        ['Hiển        —  Leader', '', '', ''],
        ['Đức         —  Senior  (dẫn khách xem đất)', '', '', ''],
        ['Sơn         —  Senior  (dẫn khách xem đất)', '', '', ''],
        ['Tuấn Anh   —  Junior   (dẫn khách xem đất)', '', '', ''],
        # row 79 — trống
        ['', '', '', ''],
        # row 80 — section header: QUY TẮC
        ['QUY TẮC CHĂM SÓC KHÁCH', '', '', ''],
        # row 81–84
        ['Lead mới  (<1h)    :  Gọi NGAY — không để qua ngày', '', '', ''],
        ['Chưa nghe máy       :  Nhắn Zalo, gọi lại sau 2 tiếng', '', '', ''],
        ['Quá 3 ngày          :  ƯU TIÊN XỬ LÝ NGAY', '', '', ''],
        ['Đã xem đất >3 ngày  :  Hỏi thăm + gửi thêm thông tin pháp lý', '', '', ''],
        # row 85 — trống
        ['', '', '', ''],
        # row 86 — section header: LƯU Ý
        ['LƯU Ý QUAN TRỌNG', '', '', ''],
        # row 87–90
        ['KHÔNG tự xóa dữ liệu trong sheet', '', '', ''],
        ['KHÔNG sửa tên tab / chia sẻ link sheet ra ngoài', '', '', ''],
        ['Mọi thay đổi lớn: báo Hiển trước khi thực hiện', '', '', ''],
        ['Dữ liệu đồng bộ real-time — mọi người đều thấy ngay', '', '', ''],
    ]
    ws.update(values=guide_data, range_name='I56:L90', value_input_option='USER_ENTERED')
    print('Đã ghi User Guide content (I56:L90).')

    # ── 4. Xây dựng batch requests định dạng ─────────────────────────────────
    requests = []

    # 4a. Freeze header row 1
    requests.append({'updateSheetProperties': {
        'properties': {'sheetId': sid,
                       'gridProperties': {'frozenRowCount': 1}},
        'fields': 'gridProperties.frozenRowCount',
    }})

    # 4b. Header format (A1:H1)
    requests.append(repeat_cell(
        sid, 0, 1, 0, 8,
        cell_format(bg=HEADER_BG, fg=HEADER_TEXT, bold=True,
                    font_size=11, h_align='CENTER'),
        fields='userEnteredFormat(backgroundColor,textFormat,horizontalAlignment,verticalAlignment,wrapStrategy)',
    ))

    # 4c. Header row height
    requests.append(dim_req(sid, 'ROWS', 0, 1, 44))

    # 4d. Xóa banding cũ (nếu có)
    meta = sp.fetch_sheet_metadata()
    for sheet_meta in meta.get('sheets', []):
        if sheet_meta['properties']['sheetId'] == sid:
            for band in sheet_meta.get('bandedRanges', []):
                requests.append({'deleteBanding': {'bandedRangeId': band['bandedRangeId']}})

    # 4e. Banding data rows (A2:H200) — dự phòng 200 dòng cho sau này
    requests.append({'addBanding': {
        'bandedRange': {
            'range': {'sheetId': sid, 'startRowIndex': 1, 'endRowIndex': 200,
                      'startColumnIndex': 0, 'endColumnIndex': 8},
            'rowProperties': {
                'headerColor':     rgb(HEADER_BG),
                'firstBandColor':  rgb(ROW_ODD),
                'secondBandColor': rgb(ROW_EVEN),
            },
        }
    }})

    # 4f. Data rows font + wrap base (A2:H200)
    requests.append(repeat_cell(
        sid, 1, 200, 0, 8,
        cell_format(font_size=10, v_align='MIDDLE'),
        fields='userEnteredFormat(textFormat,verticalAlignment,wrapStrategy)',
    ))

    # 4g. Căn chỉnh cột: B C D E G H = CENTER; A F = LEFT
    for (c1, c2), align in [
        ((1, 5), 'CENTER'),   # B–E
        ((6, 8), 'CENTER'),   # G–H
        ((0, 1), 'LEFT'),     # A
        ((5, 6), 'LEFT'),     # F
    ]:
        requests.append(repeat_cell(
            sid, 1, 200, c1, c2,
            {'horizontalAlignment': align},
            fields='userEnteredFormat.horizontalAlignment',
        ))

    # 4h. Độ rộng cột A:H
    col_widths = [160, 130, 120, 120, 130, 240, 120, 130]
    for i, w in enumerate(col_widths):
        requests.append(dim_req(sid, 'COLUMNS', i, i + 1, w))

    # 4i. Border bảng dữ liệu (A1:H200)
    requests.append(borders_req(sid, 0, 200, 0, 8, BORDER_OUTER, BORDER_INNER))

    # 4j. Conditional formatting theo Trạng thái (cột E = index 4)
    # Cột E = $E, check từng hàng
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
                'ranges': [{'sheetId': sid, 'startRowIndex': 1, 'endRowIndex': 200,
                            'startColumnIndex': 0, 'endColumnIndex': 8}],
                'booleanRule': {
                    'condition': {
                        'type': 'CUSTOM_FORMULA',
                        'values': [{'userEnteredValue': f'=$E2="{status}"'}],
                    },
                    'format': {'backgroundColor': rgb(color)},
                }
            },
            'index': 0,
        }})

    # ── 5. Định dạng User Guide ───────────────────────────────────────────────
    # Cột I=8, J=9, K=10, L=11 (0-indexed)
    # Hàng 56=55, 57=56, ... (0-indexed = row_number - 1)

    # 5a. Độ rộng cột I (index 8): 260px; J,K,L mỏng
    requests.append(dim_req(sid, 'COLUMNS', 8, 9, 260))  # I
    for col in [9, 10, 11]:                               # J, K, L
        requests.append(dim_req(sid, 'COLUMNS', col, col + 1, 20))

    # 5b. Merge tiêu đề I56:L56 (rows 55–56, cols 8–12)
    requests.append(merge_req(sid, 55, 56, 8, 12))
    # 5c. Format tiêu đề I56
    requests.append(repeat_cell(
        sid, 55, 56, 8, 12,
        cell_format(bg=GUIDE_HEADER_BG, fg='#FFFFFF', bold=True,
                    font_size=13, h_align='CENTER'),
        fields='userEnteredFormat(backgroundColor,textFormat,horizontalAlignment,verticalAlignment,wrapStrategy)',
    ))
    requests.append(dim_req(sid, 'ROWS', 55, 56, 44))

    # 5d. Merge + format I57 (phụ đề)
    requests.append(merge_req(sid, 56, 57, 8, 12))
    requests.append(repeat_cell(
        sid, 56, 57, 8, 12,
        cell_format(bg=GUIDE_META_BG, fg='#0D47A1', italic=True,
                    font_size=9, h_align='CENTER'),
        fields='userEnteredFormat(backgroundColor,textFormat,horizontalAlignment,verticalAlignment,wrapStrategy)',
    ))
    requests.append(dim_req(sid, 'ROWS', 56, 57, 26))

    # 5e. Section headers — merge + format
    # Rows (0-indexed): 58=I59, 65=I66, 70=I71, 73=I74, 79=I80, 85=I86
    section_rows = [58, 65, 70, 73, 79, 85]
    for r in section_rows:
        requests.append(merge_req(sid, r, r + 1, 8, 12))
        requests.append(repeat_cell(
            sid, r, r + 1, 8, 12,
            cell_format(bg=GUIDE_SECTION_BG, fg=GUIDE_SECTION_FG,
                        bold=True, font_size=10, h_align='LEFT'),
            fields='userEnteredFormat(backgroundColor,textFormat,horizontalAlignment,verticalAlignment,wrapStrategy)',
        ))
        requests.append(dim_req(sid, 'ROWS', r, r + 1, 28))

    # 5f. Màu trạng thái trong user guide (rows 59–63, 0-indexed)
    status_guide_colors = [C_MOI, C_CHAM, C_HEN, C_CHOT, C_TU_CHOI]
    for i, color in enumerate(status_guide_colors):
        r = 59 + i
        requests.append(merge_req(sid, r, r + 1, 8, 12))
        requests.append(repeat_cell(
            sid, r, r + 1, 8, 12,
            cell_format(bg=color, font_size=10, h_align='LEFT'),
            fields='userEnteredFormat(backgroundColor,textFormat,horizontalAlignment,verticalAlignment,wrapStrategy)',
        ))

    # 5g. Merge content rows (các dòng không phải section header, không phải trạng thái)
    # Row 72 (I72), 75–78, 81–84, 87–90
    merge_content_rows = [71, 74, 75, 76, 77, 80, 81, 82, 83, 86, 87, 88, 89]
    for r in merge_content_rows:
        requests.append(merge_req(sid, r, r + 1, 8, 12))
        requests.append(repeat_cell(
            sid, r, r + 1, 8, 12,
            cell_format(font_size=10, h_align='LEFT'),
            fields='userEnteredFormat(textFormat,horizontalAlignment,verticalAlignment,wrapStrategy)',
        ))

    # 5h. Border nhẹ quanh User Guide (I56:L90 = rows 55–90, cols 8–12)
    requests.append({'updateBorders': {
        'range': {'sheetId': sid, 'startRowIndex': 55, 'endRowIndex': 90,
                  'startColumnIndex': 8, 'endColumnIndex': 12},
        'top':    solid_border(BORDER_OUTER, 2),
        'bottom': solid_border(BORDER_OUTER, 2),
        'left':   solid_border(BORDER_OUTER, 2),
        'right':  solid_border(BORDER_OUTER, 2),
        'innerHorizontal': solid_border(GUIDE_BORDER),
        'innerVertical':   solid_border(GUIDE_BORDER),
    }})

    # ── 6. Gửi tất cả requests ────────────────────────────────────────────────
    print(f'Đang gửi {len(requests)} yêu cầu định dạng...')
    sp.batch_update({'requests': requests})
    print('Hoàn thành! Tab đã được tạo và định dạng.')
    print(f'Link: https://docs.google.com/spreadsheets/d/{SHEET_ID}/')


if __name__ == '__main__':
    main()
