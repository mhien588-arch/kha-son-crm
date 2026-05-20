"""
Áp định dạng chuyên nghiệp + User Guide vào KhaSonGreenHome_CRM (giữ nguyên data),
sau đó xóa tab rỗng "Khach_Hang_Ban2 DA KS".
"""
import os
import gspread
from google.oauth2.service_account import Credentials

SCOPES    = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
CREDS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'google_creds.json')
SHEET_ID  = '1syWcPK_YopGk2XtIYegDgHwnR6YPOHOoZmiN4ze-yjA'
CRM_TAB   = 'KhaSonGreenHome_CRM'
DEL_TAB   = 'Khach_Hang_Ban2 DA KS'

# ── Bảng màu ──────────────────────────────────────────────────────────────────
HEADER_BG        = '#0D47A1'
HEADER_TEXT      = '#FFFFFF'
ROW_ODD          = '#E8F4FD'
ROW_EVEN         = '#FFFFFF'
C_MOI            = '#E3F2FD'
C_CHAM           = '#FFF9C4'
C_HEN            = '#FFE0B2'
C_CHOT           = '#C8E6C9'
C_TU_CHOI        = '#EEEEEE'
BORDER_OUTER     = '#1565C0'
BORDER_INNER     = '#90CAF9'
GUIDE_HEADER_BG  = '#0D47A1'
GUIDE_SECTION_BG = '#E3F2FD'
GUIDE_SECTION_FG = '#0D47A1'
GUIDE_META_BG    = '#BBDEFB'
GUIDE_BORDER     = '#90CAF9'
# ──────────────────────────────────────────────────────────────────────────────


def rgb(h):
    h = h.lstrip('#')
    return {'red': int(h[0:2], 16)/255, 'green': int(h[2:4], 16)/255, 'blue': int(h[4:6], 16)/255}


def solid_border(color, width=1):
    return {'style': 'SOLID', 'width': width, 'color': rgb(color)}


def repeat_cell(sid, r1, r2, c1, c2, fmt, fields='userEnteredFormat'):
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
        'range': {'sheetId': sid, 'dimension': dimension, 'startIndex': start, 'endIndex': end},
        'properties': {'pixelSize': size},
        'fields': 'pixelSize',
    }}


def cell_fmt(bg=None, fg=None, bold=False, italic=False, font_size=10,
             h_align='LEFT', v_align='MIDDLE', wrap=True):
    fmt = {
        'textFormat': {'bold': bold, 'italic': italic,
                       'fontSize': font_size, 'fontFamily': 'Arial'},
        'horizontalAlignment': h_align,
        'verticalAlignment':   v_align,
        'wrapStrategy':        'WRAP' if wrap else 'OVERFLOW_CELL',
    }
    if bg:
        fmt['backgroundColor'] = rgb(bg)
    if fg:
        fmt['textFormat']['foregroundColor'] = rgb(fg)
    return fmt


def main():
    creds  = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
    client = gspread.authorize(creds)
    sp     = client.open_by_key(SHEET_ID)
    ws     = sp.worksheet(CRM_TAB)
    sid    = ws.id

    # Đếm dòng thực tế (bao gồm header)
    all_vals  = ws.get_all_values()
    data_rows = max(len(all_vals) - 1, 1)   # số dòng data (trừ header)
    END_ROW   = data_rows + 1               # 1-based row cuối data; 0-indexed endRowIndex = END_ROW
    print(f'CRM tab: {data_rows} dòng data (rows 2–{data_rows+1}), sheet_id={sid}')

    # ── Ghi User Guide (I56:L90) ─────────────────────────────────────────────
    guide_data = [
        ['═══  HƯỚNG DẪN SỬ DỤNG  —  KHA SƠN GREEN HOME  ═══', '', '', ''],
        ['Dự án Đất nền KCN Phú Bình, Thái Nguyên  |  Triển khai từ: 17/05/2026  |  Hotline: 0368.557.832', '', '', ''],
        ['', '', '', ''],
        ['MÀU SẮC TRẠNG THÁI', '', '', ''],
        ['Mới           → Nền xanh dương nhạt  —  Chưa liên hệ', '', '', ''],
        ['Đang chăm sóc → Nền vàng nhạt         —  Đang theo dõi', '', '', ''],
        ['Hẹn xem đất   → Nền cam nhạt           —  Đã hẹn lịch đi xem đất', '', '', ''],
        ['Chốt cọc      → Nền xanh lá nhạt       —  Đã đặt cọc  (THẮNG)', '', '', ''],
        ['Từ chối       → Nền xám nhạt           —  Không mua  (thua)', '', '', ''],
        ['', '', '', ''],
        ['QUY TRÌNH CẬP NHẬT HÀNG NGÀY', '', '', ''],
        ['Sáng  (8:00)  —  Mở Mo Tracker.bat → [3] Kiểm tra khách quá 3 ngày → Gọi ngay', '', '', ''],
        ['Chiều (17:00) —  Mở Mo Tracker.bat → [5] Cập nhật trạng thái khách', '', '', ''],
        ['Tối   (18:00) —  Mở Bao Cao Ngay.bat → Xem KPI → Chụp màn hình gửi Zalo team', '', '', ''],
        ['', '', '', ''],
        ['TRẠNG THÁI HỢP LỆ  (chỉ nhập đúng 1 trong 5 giá trị)', '', '', ''],
        ['Mới   |   Đang chăm sóc   |   Hẹn xem đất   |   Chốt cọc   |   Từ chối', '', '', ''],
        ['', '', '', ''],
        ['PHÂN CÔNG SALE', '', '', ''],
        ['Hiển        —  Leader', '', '', ''],
        ['Đức         —  Senior  (dẫn khách xem đất)', '', '', ''],
        ['Sơn         —  Senior  (dẫn khách xem đất)', '', '', ''],
        ['Tuấn Anh   —  Junior   (dẫn khách xem đất)', '', '', ''],
        ['', '', '', ''],
        ['QUY TẮC CHĂM SÓC KHÁCH', '', '', ''],
        ['Lead mới  (<1h)    :  Gọi NGAY — không để qua ngày', '', '', ''],
        ['Chưa nghe máy       :  Nhắn Zalo, gọi lại sau 2 tiếng', '', '', ''],
        ['Quá 3 ngày          :  ƯU TIÊN XỬ LÝ NGAY', '', '', ''],
        ['Đã xem đất >3 ngày  :  Hỏi thăm + gửi thêm thông tin pháp lý', '', '', ''],
        ['', '', '', ''],
        ['LƯU Ý QUAN TRỌNG', '', '', ''],
        ['KHÔNG tự xóa dữ liệu trong sheet', '', '', ''],
        ['KHÔNG sửa tên tab / chia sẻ link sheet ra ngoài', '', '', ''],
        ['Mọi thay đổi lớn: báo Hiển trước khi thực hiện', '', '', ''],
        ['Dữ liệu đồng bộ real-time — mọi người đều thấy ngay', '', '', ''],
    ]
    ws.update(values=guide_data, range_name='I56:L90', value_input_option='USER_ENTERED')
    print('Đã ghi User Guide (I56:L90).')

    # ── Build batch requests ──────────────────────────────────────────────────
    reqs = []

    # 1. Freeze header
    reqs.append({'updateSheetProperties': {
        'properties': {'sheetId': sid, 'gridProperties': {'frozenRowCount': 1}},
        'fields': 'gridProperties.frozenRowCount',
    }})

    # 2. Header format (A1:H1)
    reqs.append(repeat_cell(
        sid, 0, 1, 0, 8,
        cell_fmt(bg=HEADER_BG, fg=HEADER_TEXT, bold=True, font_size=11, h_align='CENTER'),
        fields='userEnteredFormat(backgroundColor,textFormat,horizontalAlignment,verticalAlignment,wrapStrategy)',
    ))

    # 3. Header row height
    reqs.append(dim_req(sid, 'ROWS', 0, 1, 44))

    # 4. Xóa banding cũ
    meta = sp.fetch_sheet_metadata()
    for sheet_info in meta.get('sheets', []):
        if sheet_info['properties']['sheetId'] == sid:
            for band in sheet_info.get('bandedRanges', []):
                reqs.append({'deleteBanding': {'bandedRangeId': band['bandedRangeId']}})

    # 5. Xóa conditional formatting cũ
    for sheet_info in meta.get('sheets', []):
        if sheet_info['properties']['sheetId'] == sid:
            rules = sheet_info.get('conditionalFormats', [])
            for _ in rules:
                reqs.append({'deleteConditionalFormatRule': {'sheetId': sid, 'index': 0}})

    # 6. Banding data rows (A2:H200)
    reqs.append({'addBanding': {
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

    # 7. Data rows font + wrap
    reqs.append(repeat_cell(
        sid, 1, 200, 0, 8,
        cell_fmt(font_size=10),
        fields='userEnteredFormat(textFormat,verticalAlignment,wrapStrategy)',
    ))

    # 8. Căn chỉnh cột
    for (c1, c2), align in [
        ((1, 5), 'CENTER'),
        ((6, 8), 'CENTER'),
        ((0, 1), 'LEFT'),
        ((5, 6), 'LEFT'),
    ]:
        reqs.append(repeat_cell(
            sid, 1, 200, c1, c2,
            {'horizontalAlignment': align},
            fields='userEnteredFormat.horizontalAlignment',
        ))

    # 9. Độ rộng cột A:H
    for i, w in enumerate([160, 130, 120, 120, 130, 240, 120, 130]):
        reqs.append(dim_req(sid, 'COLUMNS', i, i + 1, w))

    # 10. Border bảng dữ liệu
    reqs.append({'updateBorders': {
        'range': {'sheetId': sid, 'startRowIndex': 0, 'endRowIndex': 200,
                  'startColumnIndex': 0, 'endColumnIndex': 8},
        'top':    solid_border(BORDER_OUTER, 2), 'bottom': solid_border(BORDER_OUTER, 2),
        'left':   solid_border(BORDER_OUTER, 2), 'right':  solid_border(BORDER_OUTER, 2),
        'innerHorizontal': solid_border(BORDER_INNER),
        'innerVertical':   solid_border(BORDER_INNER),
    }})

    # 11. Conditional formatting theo Trạng thái (cột E)
    for status, color in [
        ('Chốt cọc',        C_CHOT),
        ('Hẹn xem đất',     C_HEN),
        ('Đang chăm sóc',   C_CHAM),
        ('Từ chối',         C_TU_CHOI),
        ('Mới',             C_MOI),
    ]:
        reqs.append({'addConditionalFormatRule': {
            'rule': {
                'ranges': [{'sheetId': sid, 'startRowIndex': 1, 'endRowIndex': 200,
                            'startColumnIndex': 0, 'endColumnIndex': 8}],
                'booleanRule': {
                    'condition': {'type': 'CUSTOM_FORMULA',
                                  'values': [{'userEnteredValue': f'=$E2="{status}"'}]},
                    'format': {'backgroundColor': rgb(color)},
                },
            },
            'index': 0,
        }})

    # ── User Guide formatting (I56:L90) ──────────────────────────────────────
    # Cột I=8 J=9 K=10 L=11; rows: 56→55, 57→56 ... (0-indexed = row_number-1)

    # Độ rộng cột I và J,K,L
    reqs.append(dim_req(sid, 'COLUMNS', 8, 9, 260))
    for col in [9, 10, 11]:
        reqs.append(dim_req(sid, 'COLUMNS', col, col + 1, 20))

    # Tiêu đề chính I56 (row 55, 0-indexed)
    reqs.append(merge_req(sid, 55, 56, 8, 12))
    reqs.append(repeat_cell(
        sid, 55, 56, 8, 12,
        cell_fmt(bg=GUIDE_HEADER_BG, fg='#FFFFFF', bold=True, font_size=13, h_align='CENTER'),
        fields='userEnteredFormat(backgroundColor,textFormat,horizontalAlignment,verticalAlignment,wrapStrategy)',
    ))
    reqs.append(dim_req(sid, 'ROWS', 55, 56, 44))

    # Phụ đề I57 (row 56)
    reqs.append(merge_req(sid, 56, 57, 8, 12))
    reqs.append(repeat_cell(
        sid, 56, 57, 8, 12,
        cell_fmt(bg=GUIDE_META_BG, fg='#0D47A1', italic=True, font_size=9, h_align='CENTER'),
        fields='userEnteredFormat(backgroundColor,textFormat,horizontalAlignment,verticalAlignment,wrapStrategy)',
    ))
    reqs.append(dim_req(sid, 'ROWS', 56, 57, 26))

    # Section headers: I59=row58, I66=row65, I71=row70, I74=row73, I80=row79, I86=row85
    for r in [58, 65, 70, 73, 79, 85]:
        reqs.append(merge_req(sid, r, r + 1, 8, 12))
        reqs.append(repeat_cell(
            sid, r, r + 1, 8, 12,
            cell_fmt(bg=GUIDE_SECTION_BG, fg=GUIDE_SECTION_FG, bold=True,
                     font_size=10, h_align='LEFT'),
            fields='userEnteredFormat(backgroundColor,textFormat,horizontalAlignment,verticalAlignment,wrapStrategy)',
        ))
        reqs.append(dim_req(sid, 'ROWS', r, r + 1, 28))

    # Màu trạng thái: I60–I64 (rows 59–63)
    for i, color in enumerate([C_MOI, C_CHAM, C_HEN, C_CHOT, C_TU_CHOI]):
        r = 59 + i
        reqs.append(merge_req(sid, r, r + 1, 8, 12))
        reqs.append(repeat_cell(
            sid, r, r + 1, 8, 12,
            cell_fmt(bg=color, font_size=10, h_align='LEFT'),
            fields='userEnteredFormat(backgroundColor,textFormat,horizontalAlignment,verticalAlignment,wrapStrategy)',
        ))

    # Merge content rows còn lại
    for r in [71, 74, 75, 76, 77, 80, 81, 82, 83, 86, 87, 88, 89]:
        reqs.append(merge_req(sid, r, r + 1, 8, 12))
        reqs.append(repeat_cell(
            sid, r, r + 1, 8, 12,
            cell_fmt(font_size=10, h_align='LEFT'),
            fields='userEnteredFormat(textFormat,horizontalAlignment,verticalAlignment,wrapStrategy)',
        ))

    # Border User Guide
    reqs.append({'updateBorders': {
        'range': {'sheetId': sid, 'startRowIndex': 55, 'endRowIndex': 90,
                  'startColumnIndex': 8, 'endColumnIndex': 12},
        'top':    solid_border(BORDER_OUTER, 2), 'bottom': solid_border(BORDER_OUTER, 2),
        'left':   solid_border(BORDER_OUTER, 2), 'right':  solid_border(BORDER_OUTER, 2),
        'innerHorizontal': solid_border(GUIDE_BORDER),
        'innerVertical':   solid_border(GUIDE_BORDER),
    }})

    # ── Gửi tất cả requests ───────────────────────────────────────────────────
    print(f'Đang gửi {len(reqs)} yêu cầu định dạng...')
    sp.batch_update({'requests': reqs})
    print('Định dạng CRM tab hoàn thành.')

    # ── Xóa tab rỗng ─────────────────────────────────────────────────────────
    tabs = {ws2.title: ws2 for ws2 in sp.worksheets()}
    if DEL_TAB in tabs:
        sp.del_worksheet(tabs[DEL_TAB])
        print(f'Đã xóa tab: "{DEL_TAB}"')
    else:
        print(f'Tab "{DEL_TAB}" không tồn tại, bỏ qua.')

    print(f'\nLink: https://docs.google.com/spreadsheets/d/{SHEET_ID}/')


if __name__ == '__main__':
    main()
