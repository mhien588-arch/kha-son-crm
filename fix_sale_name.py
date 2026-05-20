"""Đổi 'TA' -> 'Tuấn Anh' trong cột Sale chăm sóc trên Google Sheets."""
import os, gspread
from google.oauth2.service_account import Credentials

SCOPES = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']
creds = Credentials.from_service_account_file('data/google_creds.json', scopes=SCOPES)
client = gspread.authorize(creds)
ws = client.open_by_key('1syWcPK_YopGk2XtIYegDgHwnR6YPOHOoZmiN4ze-yjA').worksheet('KhaSonGreenHome_CRM')

rows = ws.get_all_values()
data = rows[1:]  # bỏ header

updates = []
for i, r in enumerate(data, 2):  # row 2 trở đi
    if len(r) >= 4 and r[3].strip() == 'TA':
        updates.append({'range': f'D{i}', 'values': [['Tuấn Anh']]})

if not updates:
    print('Khong co dong nao can sua.')
else:
    ws.batch_update(updates)
    print(f'Da sua {len(updates)} dong: TA -> Tuan Anh')
    for u in updates:
        row_idx = int(u['range'][1:])
        ten = rows[row_idx - 1][0] if row_idx - 1 < len(rows) else '?'
        print(f'  {u["range"]}: {ten}')
