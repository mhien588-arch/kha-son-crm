"""
Re-import dữ liệu từ sheet nguồn mới vào CRM — có date forward-fill logic
Nguồn: 1h279Q2vg3krxnoO7vR3uq70KZHGilXQNdV4PZeouGLU (Sheet1)
CRM:   1syWcPK_YopGk2XtIYegDgHwnR6YPOHOoZmiN4ze-yjA (KhaSonGreenHome_CRM)
"""
import os, gspread
from google.oauth2.service_account import Credentials

SCOPES    = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
CREDS     = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'google_creds.json')
SRC_ID    = '1h279Q2vg3krxnoO7vR3uq70KZHGilXQNdV4PZeouGLU'
CRM_ID    = '1syWcPK_YopGk2XtIYegDgHwnR6YPOHOoZmiN4ze-yjA'
CRM_WS    = 'KhaSonGreenHome_CRM'

# ── Mapping ───────────────────────────────────────────────
STATUS_MAP = {
    'da gioi thieu chung': 'Dang cham soc',
    'hen gap':             'Hen xem dat',
    'da tham du an':       'Hen xem dat',
    'chua lien lac':       'Moi',
}
STATUS_VN = {
    'Đã giới thiệu chung': 'Đang chăm sóc',
    'Hẹn gặp':             'Hẹn xem đất',
    'Đã thăm dự án':       'Hẹn xem đất',
    'Chưa liên lạc':       'Mới',
}

def map_status(raw):
    return STATUS_VN.get(raw.strip(), 'Mới' if not raw.strip() else 'Đang chăm sóc')

def map_sale(raw):
    raw = raw.strip()
    first = raw.split(',')[0].strip()
    if first.upper() == 'TA':
        return 'Tuấn Anh'
    return first

def parse_date(s):
    """'18/03' hoặc '6/4' → '2026-03-18'"""
    s = s.strip()
    if not s or s.lower().startswith('so') or 'c' in s.lower():
        return None
    parts = s.replace('-', '/').split('/')
    if len(parts) < 2:
        return None
    try:
        day, month = int(parts[0]), int(parts[1])
        return f'2026-{month:02d}-{day:02d}'
    except ValueError:
        return None

def build_ghi_chu(chan_dung, noi_o, muc_do):
    parts = []
    if muc_do.strip():
        parts.append('MD: ' + muc_do.strip())
    if chan_dung.strip():
        parts.append(chan_dung.strip())
    if noi_o.strip():
        parts.append('Noi: ' + noi_o.strip())
    return ' | '.join(parts)

def main():
    creds_obj = Credentials.from_service_account_file(CREDS, scopes=SCOPES)
    client    = gspread.authorize(creds_obj)

    # ── Đọc nguồn ────────────────────────────────────────
    src_ws = client.open_by_key(SRC_ID).get_worksheet(0)
    all_rows = src_ws.get_all_values()
    data_rows = all_rows[2:]  # bỏ row 1 (title) + row 2 (header)
    print(f'Sheet nguon: {len(data_rows)} hang du lieu')

    # ── Xác định điểm bắt đầu forward-fill (R13 = index 10 trong data_rows) ──
    # data_rows[0] = R3, data_rows[10] = R13
    DATE_START_IDX = 10  # từ data_rows[10] (tương ứng R13) trở đi mới forward-fill

    # ── Parse từng hàng ──────────────────────────────────
    crm_rows   = []
    skipped    = 0
    current_date = ''
    date_started = False  # True khi gặp ngày đầu tiên (R13 trở đi)

    for i, r in enumerate(data_rows):
        r = (r + [''] * 16)[:16]
        col_a, _, ten, chan_dung, noi_o, sdt, nguon, muc_do, tinh_trang, sale_raw = r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8], r[9]

        # Skip hàng không có tên lẫn số ĐT thực sự
        ten = ten.strip()
        sdt = sdt.strip()
        if not ten and (not sdt or not any(c.isdigit() for c in sdt)):
            skipped += 1
            continue

        # ── Xác định ngày ────────────────────────────────
        col_a_val = col_a.strip()
        is_so_ca_nhan = col_a_val.lower().startswith('so') or 'cá nhân' in col_a_val.lower()

        if is_so_ca_nhan:
            ngay = ''
        elif col_a_val and not is_so_ca_nhan:
            parsed = parse_date(col_a_val)
            if parsed:
                current_date = parsed
                date_started = True
            ngay = current_date
        else:
            # col_a trống
            if i >= DATE_START_IDX and date_started:
                ngay = current_date  # forward-fill
            else:
                ngay = ''            # trước khi có ngày đầu tiên

        # ── Map các trường ────────────────────────────────
        trang_thai = map_status(tinh_trang)
        sale       = map_sale(sale_raw)
        ghi_chu    = build_ghi_chu(chan_dung, noi_o, muc_do)

        crm_rows.append([
            ten,
            sdt,
            nguon.strip() or 'Khách cũ',
            sale,
            trang_thai,
            ghi_chu,
            ngay,
            ngay,  # Ngày tương tác cuối = Ngày tiếp cận
        ])

    print(f'Hop le: {len(crm_rows)} hang | Bo qua: {skipped} hang')

    # ── Xóa data CRM (giữ format) + ghi mới ──────────────
    crm_ws = client.open_by_key(CRM_ID).worksheet(CRM_WS)
    crm_ws.batch_clear(['A2:H200'])
    print('Da xoa du lieu cu (giu dinh dang).')

    end_row = 1 + len(crm_rows)
    crm_ws.update(f'A2:H{end_row}', crm_rows, value_input_option='USER_ENTERED')
    print(f'Da ghi {len(crm_rows)} hang vao CRM (A2:H{end_row}).')

    # ── Báo cáo ───────────────────────────────────────────
    from collections import Counter
    sales = Counter(r[3] for r in crm_rows)
    statuses = Counter(r[4] for r in crm_rows)
    dated = sum(1 for r in crm_rows if r[6])
    no_date = sum(1 for r in crm_rows if not r[6])

    print('\n=== KET QUA ===')
    print(f'Tong khach: {len(crm_rows)}')
    print('Phan bo sale:')
    for s, c in sorted(sales.items()):
        print(f'  {s}: {c}')
    print('Trang thai:')
    for s, c in sorted(statuses.items()):
        print(f'  {s}: {c}')
    print(f'Co ngay: {dated} | Khong ngay: {no_date}')
    print('\nHoan thanh!')

if __name__ == '__main__':
    main()
