"""
Tái tạo User Guide đầy đủ tại M56:P90 (cột 12–15) với toàn bộ màu sắc, merge, border.
Xóa sạch I56:L90 và M56:P90 trước khi ghi mới.
Chạy một lần: python recreate_user_guide_m56.py
"""
import os
import gspread
from google.oauth2.service_account import Credentials

SCOPES     = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
CREDS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'google_creds.json')
SHEET_ID   = '1syWcPK_YopGk2XtIYegDgHwnR6YPOHOoZmiN4ze-yjA'
CRM_TAB    = 'KhaSonGreenHome_CRM'

# Cột đích: M=12, N=13, O=14, P=15  (0-indexed)
C1, C2 = 12, 16   # startColumnIndex, endColumnIndex

# Bảng màu (giống apply_format_crm.py)
HEADER_BG        = '#0D47A1'
C_MOI            = '#E3F2FD'
C_CHAM           = '#FFF9C4'
C_HEN            = '#FFE0B2'
C_CHOT           = '#C8E6C9'
C_TU_CHOI        = '#EEEEEE'
GUIDE_SECTION_BG = '#E3F2FD'
GUIDE_SECTION_FG = '#0D47A1'
GUIDE_META_BG    = '#BBDEFB'
BORDER_OUTER     = '#1565C0'
GUIDE_BORDER     = '#90CAF9'


def rgb(h):
    h = h.lstrip('#')
    return {'red': int(h[0:2], 16)/255, 'green': int(h[2:4], 16)/255, 'blue': int(h[4:6], 16)/255}


def solid_border(color, width=1):
    return {'style': 'SOLID', 'width': width, 'color': rgb(color)}


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


def main():
    creds  = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
    client = gspread.authorize(creds)
    sp     = client.open_by_key(SHEET_ID)
    ws     = sp.worksheet(CRM_TAB)
    sid    = ws.id

    # Xóa sạch cả hai vùng cũ trước khi ghi mới
    print("Xóa I56:L90 và M56:P90...")
    ws.batch_clear(["I56:L90", "M56:P90"])

    # Ghi nội dung User Guide vào M56:P90
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
    ws.update(values=guide_data, range_name='M56:P90', value_input_option='USER_ENTERED')
    print("Đã ghi nội dung vào M56:P90.")

    reqs = []

    # Độ rộng cột M (rộng) và N,O,P (hẹp để merge trông đẹp)
    reqs.append(dim_req(sid, 'COLUMNS', 12, 13, 260))
    for col in [13, 14, 15]:
        reqs.append(dim_req(sid, 'COLUMNS', col, col + 1, 20))

    # ── Tiêu đề chính M56 (row 55, 0-indexed) ──
    reqs.append(merge_req(sid, 55, 56, C1, C2))
    reqs.append(repeat_cell(
        sid, 55, 56, C1, C2,
        cell_fmt(bg=HEADER_BG, fg='#FFFFFF', bold=True, font_size=13, h_align='CENTER'),
        fields='userEnteredFormat(backgroundColor,textFormat,horizontalAlignment,verticalAlignment,wrapStrategy)',
    ))
    reqs.append(dim_req(sid, 'ROWS', 55, 56, 44))

    # ── Phụ đề M57 (row 56) ──
    reqs.append(merge_req(sid, 56, 57, C1, C2))
    reqs.append(repeat_cell(
        sid, 56, 57, C1, C2,
        cell_fmt(bg=GUIDE_META_BG, fg='#0D47A1', italic=True, font_size=9, h_align='CENTER'),
        fields='userEnteredFormat(backgroundColor,textFormat,horizontalAlignment,verticalAlignment,wrapStrategy)',
    ))
    reqs.append(dim_req(sid, 'ROWS', 56, 57, 26))

    # ── Section headers: rows 58, 65, 70, 73, 79, 85 (0-indexed) ──
    for r in [58, 65, 70, 73, 79, 85]:
        reqs.append(merge_req(sid, r, r + 1, C1, C2))
        reqs.append(repeat_cell(
            sid, r, r + 1, C1, C2,
            cell_fmt(bg=GUIDE_SECTION_BG, fg=GUIDE_SECTION_FG, bold=True,
                     font_size=10, h_align='LEFT'),
            fields='userEnteredFormat(backgroundColor,textFormat,horizontalAlignment,verticalAlignment,wrapStrategy)',
        ))
        reqs.append(dim_req(sid, 'ROWS', r, r + 1, 28))

    # ── Màu trạng thái: rows 59–63 ──
    for i, color in enumerate([C_MOI, C_CHAM, C_HEN, C_CHOT, C_TU_CHOI]):
        r = 59 + i
        reqs.append(merge_req(sid, r, r + 1, C1, C2))
        reqs.append(repeat_cell(
            sid, r, r + 1, C1, C2,
            cell_fmt(bg=color, font_size=10, h_align='LEFT'),
            fields='userEnteredFormat(backgroundColor,textFormat,horizontalAlignment,verticalAlignment,wrapStrategy)',
        ))

    # ── Merge các dòng nội dung còn lại ──
    for r in [71, 74, 75, 76, 77, 80, 81, 82, 83, 86, 87, 88, 89]:
        reqs.append(merge_req(sid, r, r + 1, C1, C2))
        reqs.append(repeat_cell(
            sid, r, r + 1, C1, C2,
            cell_fmt(font_size=10, h_align='LEFT'),
            fields='userEnteredFormat(textFormat,horizontalAlignment,verticalAlignment,wrapStrategy)',
        ))

    # ── Border toàn bộ vùng M56:P90 ──
    reqs.append({'updateBorders': {
        'range': {'sheetId': sid, 'startRowIndex': 55, 'endRowIndex': 90,
                  'startColumnIndex': C1, 'endColumnIndex': C2},
        'top':    solid_border(BORDER_OUTER, 2), 'bottom': solid_border(BORDER_OUTER, 2),
        'left':   solid_border(BORDER_OUTER, 2), 'right':  solid_border(BORDER_OUTER, 2),
        'innerHorizontal': solid_border(GUIDE_BORDER),
        'innerVertical':   solid_border(GUIDE_BORDER),
    }})

    print(f"Đang gửi {len(reqs)} yêu cầu định dạng...")
    sp.batch_update({'requests': reqs})
    print("✅ Xong! User Guide đầy đủ định dạng tại M56:P90.")
    print(f"Link: https://docs.google.com/spreadsheets/d/{SHEET_ID}/")


if __name__ == '__main__':
    main()
