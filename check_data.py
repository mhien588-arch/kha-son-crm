import gspread, os
from google.oauth2.service_account import Credentials

SCOPES = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']
creds = Credentials.from_service_account_file('data/google_creds.json', scopes=SCOPES)
client = gspread.authorize(creds)
ws = client.open_by_key('1syWcPK_YopGk2XtIYegDgHwnR6YPOHOoZmiN4ze-yjA').worksheet('KhaSonGreenHome_CRM')
rows = ws.get_all_values()
data = rows[1:]

print(f'Tong khach: {len(data)}\n')

issues = []
sale_values = {}
for i, r in enumerate(data, 2):
    r = (r + [''] * 8)[:8]
    ten, sdt, nguon, sale, tt, ghi_chu, ngay_tc, ngay_ttc = r
    sale = sale.strip()
    sale_values[sale] = sale_values.get(sale, 0) + 1
    probs = []
    if not ten.strip():
        probs.append('Thieu ten')
    if not sdt.strip() or not any(c.isdigit() for c in sdt):
        probs.append('SDT khong hop le: [' + sdt + ']')
    if not sale:
        probs.append('Thieu sale')
    if probs:
        issues.append((i, ten, sdt, sale, probs))

print('=== VAN DE DU LIEU ===')
if issues:
    for row, ten, sdt, sale, probs in issues:
        print('  Row ' + str(row) + ': [' + ten + '] [' + sdt + '] [' + sale + '] -> ' + ', '.join(probs))
else:
    print('  Khong co van de!')

print('\n=== GIA TRI COT SALE ===')
for s in sorted(sale_values.keys()):
    print('  [' + s + ']: ' + str(sale_values[s]) + ' khach')
